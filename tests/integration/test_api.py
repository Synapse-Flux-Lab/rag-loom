import pytest
from fastapi.testclient import TestClient

class TestIngestionAPI:
    
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "embedding_model" in data
        assert "llm_provider" in data
        assert "ollama_model" in data
        assert "ollama_url" in data
        assert "timestamp" in data
        assert "vector_store" in data
    
    def test_ingest_pdf_file(self, client: TestClient, sample_pdf_content):
        """Test PDF file ingest endpoint"""
        files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "file_id" in data
    
    def test_ingest_txt_file(self, client: TestClient, sample_txt_content):
        """Test TXT file ingest endpoint"""
        files = {"file": ("test.txt", sample_txt_content, "text/plain")}
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "file_id" in data
    
    def test_ingest_invalid_file_type(self, client: TestClient):
        """Test ingest with invalid file type"""
        files = {"file": ("test.docx", b"invalid content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
    
    def test_ingest_no_file(self, client: TestClient):
        """Test ingest without file"""
        response = client.post("/api/v1/ingest")
        assert response.status_code == 422  # Validation error
    
    def test_ingest_empty_file(self, client: TestClient):
        """Test ingest with empty file"""
        files = {"file": ("empty.txt", b"", "text/plain")}
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 200  # Should handle empty files gracefully

    def test_ingest_batch_files(self, client: TestClient, sample_txt_content):
        """Test batch ingest endpoint processes multiple files"""
        files = [
            ("files", ("batch1.txt", sample_txt_content, "text/plain")),
            ("files", ("batch2.txt", b"Additional batch file content.", "text/plain")),
        ]

        response = client.post("/api/v1/ingest/batch", files=files)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        for item in data:
            assert item["chunks_created"] >= 0
            assert item["file_name"] in {"batch1.txt", "batch2.txt"}
            assert item["message"]
