"""Extract text from PDF files."""

import sys

import pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """Return all text from the PDF at `pdf_path`, page by page."""
    pages_text = []

    with pymupdf.open(pdf_path) as document:
        for page in document:
            pages_text.append(page.get_text())

    return "\n".join(pages_text)


if __name__ == "__main__":
    from app.skills import detect_skills

    if len(sys.argv) != 2:
        print("Usage: python -m app.parsing <path-to-pdf>")
        sys.exit(1)

    extracted_text = extract_text_from_pdf(sys.argv[1])
    print(f"Characters extracted: {len(extracted_text)}")
    print("--- First 500 characters ---")
    print(extracted_text[:500])
    print("--- Skills detected ---")
    print(detect_skills(extracted_text))