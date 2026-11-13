"""Extract text from PDF files."""

import sys

import pymupdf


class PdfParsingError(Exception):
    """Raised when a PDF cannot be read or contains no usable text."""


def _read_text(document) -> str:
    """Join the text of all pages and make sure something was found."""
    pages_text = [page.get_text() for page in document]
    text = "\n".join(pages_text).strip()
    if not text:
        raise PdfParsingError(
            "No text could be extracted. The PDF may be empty or a scanned image."
        )
    return text


def extract_text_from_pdf(pdf_path: str) -> str:
    """Return all text from the PDF file at `pdf_path`."""
    try:
        with pymupdf.open(pdf_path) as document:
            return _read_text(document)
    except RuntimeError as error:  # PyMuPDF raises RuntimeError subclasses
        raise PdfParsingError(f"Could not read the PDF file: {error}") from error


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """Return all text from PDF data held in memory (used for uploaded files)."""
    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
            return _read_text(document)
    except RuntimeError as error:
        raise PdfParsingError(f"Could not read the PDF file: {error}") from error


if __name__ == "__main__":
    from app.skills import detect_skills

    if len(sys.argv) != 2:
        print("Usage: python -m app.parsing <path-to-pdf>")
        sys.exit(1)

    try:
        extracted_text = extract_text_from_pdf(sys.argv[1])
    except PdfParsingError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"Characters extracted: {len(extracted_text)}")
    print("--- First 500 characters ---")
    print(extracted_text[:500])
    print("--- Skills detected ---")
    print(detect_skills(extracted_text))