import io

import pytest
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@pytest.fixture
def sample_pdf_content():
    """Generate an in-memory PDF payload for tests."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "(Hello World)")
    pdf.drawString(100, 730, "Test PDF Content")
    pdf.save()
    buffer.seek(0)
    payload = buffer.getvalue()
    buffer.close()
    return payload


@pytest.fixture
def sample_txt_content():
    """Provide a representative TXT payload."""
    return b"This is a sample text file for testing purposes."
