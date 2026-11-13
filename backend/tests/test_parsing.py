import pymupdf
import pytest

from app.parsing import PdfParsingError, extract_text_from_bytes, extract_text_from_pdf


def make_pdf(path, text):
    """Create a small one-page PDF for testing."""
    document = pymupdf.open()
    page = document.new_page()
    if text:
        page.insert_text((72, 72), text)
    document.save(str(path))
    document.close()


def test_extracts_text_from_valid_pdf(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    make_pdf(pdf_path, "Skills: Python and SQL")
    assert "Python and SQL" in extract_text_from_pdf(str(pdf_path))


def test_extracts_text_from_bytes(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    make_pdf(pdf_path, "Skills: Python and SQL")
    assert "Python and SQL" in extract_text_from_bytes(pdf_path.read_bytes())


def test_missing_file_raises_clear_error(tmp_path):
    with pytest.raises(PdfParsingError):
        extract_text_from_pdf(str(tmp_path / "does_not_exist.pdf"))


def test_invalid_pdf_raises_clear_error(tmp_path):
    bad_file = tmp_path / "bad.pdf"
    bad_file.write_bytes(b"this is not a pdf")
    with pytest.raises(PdfParsingError):
        extract_text_from_pdf(str(bad_file))


def test_empty_bytes_raise_clear_error():
    with pytest.raises(PdfParsingError):
        extract_text_from_bytes(b"")


def test_pdf_without_text_raises_clear_error(tmp_path):
    blank_pdf = tmp_path / "blank.pdf"
    make_pdf(blank_pdf, "")
    with pytest.raises(PdfParsingError):
        extract_text_from_pdf(str(blank_pdf))