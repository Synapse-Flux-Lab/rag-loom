import pytest
from app.utils.file_processing import FileProcessor

class TestFileProcessor:
    
    def test_extract_text_from_txt(self, sample_txt_content):
        """Test text extraction from TXT files"""
        text = FileProcessor.extract_text_from_txt(sample_txt_content)
        assert text == "This is a sample text file for testing purposes."
    
    def test_extract_text_from_pdf(self, sample_pdf_content):
        """Test text extraction from PDF files"""
        text = FileProcessor.extract_text_from_pdf(sample_pdf_content)
        assert "Hello World" in text
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  This   is   a   test   text  \n\n\n  with   extra   spaces  "
        clean_text = FileProcessor.clean_text(dirty_text)
        assert clean_text == "This is a test text with extra spaces"
    
    def test_get_file_type_pdf(self):
        """Test file type detection for PDF"""
        file_type = FileProcessor.get_file_type("document.pdf")
        assert file_type == "pdf"
    
    def test_get_file_type_txt(self):
        """Test file type detection for TXT"""
        file_type = FileProcessor.get_file_type("document.txt")
        assert file_type == "txt"
    
    def test_get_file_type_unsupported(self):
        """Test file type detection for unsupported files"""
        with pytest.raises(ValueError, match="Unsupported file type"):
            FileProcessor.get_file_type("document.docx")
    
    def test_decode_error_handling(self):
        """Test handling of encoding errors in text files"""
        # Create content with invalid encoding
        invalid_content = b'\xff\xfe\x00\x00'  # Invalid UTF-8
        with pytest.raises(ValueError, match="Failed to decode text file"):
            FileProcessor.extract_text_from_txt(invalid_content)
