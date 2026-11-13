"""FastAPI application: the entry point of the CareerLens AI backend."""

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.matching import analyze_match
from app.parsing import PdfParsingError, extract_text_from_bytes
from app.schemas import AnalysisResult

MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

app = FastAPI(title="CareerLens AI API")


@app.get("/health")
def health_check() -> dict:
    """Simple check that the server is running."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):
    """Compare an uploaded PDF resume with a pasted job description."""
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