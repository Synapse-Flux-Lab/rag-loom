import pytest
from fastapi.testclient import TestClient
import sys
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.main import app

# Add the project root directory to Python path

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing"""
    #return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    buffer = io.BytesIO()
    
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "(Hello World)")
    c.drawString(100, 730, "Test PDF Content")
    c.save()
    
    buffer.seek(0)
    content = buffer.getvalue()
    buffer.close()
    
    return content

@pytest.fixture
def sample_txt_content():
    """Sample text content for testing"""
    return b"This is a sample text file for testing purposes."
