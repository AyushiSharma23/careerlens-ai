"""FastAPI application: the entry point of the CareerLens AI backend."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, File, Form, HTTPException, Response, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.matching import analyze_match
from app.models import Analysis
from app.parsing import PdfParsingError, extract_text_from_bytes
from app.schemas import AnalysisRecord, AnalysisResult

MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database tables (if missing) when the server starts."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="CareerLens AI API", lifespan=lifespan)


async def read_and_analyze(resume: UploadFile, job_description: str) -> dict:
    """Validate the inputs, read the PDF and return the analysis result."""
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="The job description cannot be empty.")

    if not (resume.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await resume.read()
    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="The PDF is too large. Maximum size is 5 MB.")

    try:
        resume_text = extract_text_from_bytes(pdf_bytes)
    except PdfParsingError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return analyze_match(resume_text, job_description)


@app.get("/health")
def health_check() -> dict:
    """Simple check that the server is running."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):
    """Analyse a resume against a job description without saving anything."""
    return await read_and_analyze(resume, job_description)


@app.post("/analyses", response_model=AnalysisRecord, status_code=201)
async def save_analysis(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(...),
    company: str = Form(""),
    db: Session = Depends(get_db),
):
    """Analyse a resume against a job description and save the result."""
    if not job_title.strip():
        raise HTTPException(status_code=400, detail="The job title cannot be empty.")

    result = await read_and_analyze(resume, job_description)

    analysis = Analysis(
        job_title=job_title.strip(),
        company=company.strip(),
        job_description=job_description.strip(),
        **result,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@app.get("/analyses", response_model=list[AnalysisRecord])
def list_analyses(db: Session = Depends(get_db)):
    """Return all saved analyses, newest first."""
    query = select(Analysis).order_by(Analysis.created_at.desc(), Analysis.id.desc())
    return db.scalars(query).all()


@app.get("/analyses/{analysis_id}", response_model=AnalysisRecord)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Return one saved analysis."""
    analysis = db.get(Analysis, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return analysis


@app.delete("/analyses/{analysis_id}", status_code=204)
def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Delete one saved analysis."""
    analysis = db.get(Analysis, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    db.delete(analysis)
    db.commit()
    return Response(status_code=204)