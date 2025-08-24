import pytest
from fastapi.testclient import TestClient

class TestIngestionAPI:
    
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_upload_pdf_file(self, client: TestClient, sample_pdf_content):
        """Test PDF file upload endpoint"""
        files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "file_id" in data
    
    def test_upload_txt_file(self, client: TestClient, sample_txt_content):
        """Test TXT file upload endpoint"""
        files = {"file": ("test.txt", sample_txt_content, "text/plain")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "file_id" in data
    
    def test_upload_invalid_file_type(self, client: TestClient):
        """Test upload with invalid file type"""
        files = {"file": ("test.docx", b"invalid content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/upload", files=files)
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
    
    def test_upload_no_file(self, client: TestClient):
        """Test upload without file"""
        response = client.post("/upload")
        assert response.status_code == 422  # Validation error
    
    def test_upload_empty_file(self, client: TestClient):
        """Test upload with empty file"""
        files = {"file": ("empty.txt", b"", "text/plain")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200  # Should handle empty files gracefully
