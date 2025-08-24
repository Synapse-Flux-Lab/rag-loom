#!/usr/bin/env python3
"""
Manual test script for testing the RAG API endpoints
Run this after starting your service locally
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_PDF_CONTENT = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
TEST_TXT_CONTENT = b"This is a sample text file for testing purposes."

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
        else:
            print("❌ Health check failed:", response.status_code, response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to service. Is it running?")
        return False
    return True

def test_upload_pdf():
    """Test PDF file upload"""
    print("\n📄 Testing PDF upload...")
    try:
        files = {"file": ("test.pdf", TEST_PDF_CONTENT, "application/pdf")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code == 200:
            print("✅ PDF upload successful:", response.json())
        else:
            print("❌ PDF upload failed:", response.status_code, response.text)
    except Exception as e:
        print(f"❌ PDF upload error: {e}")

def test_upload_txt():
    """Test TXT file upload"""
    print("\n📝 Testing TXT upload...")
    try:
        files = {"file": ("test.txt", TEST_TXT_CONTENT, "text/plain")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code == 200:
            print("✅ TXT upload successful:", response.json())
        else:
            print("❌ TXT upload failed:", response.status_code, response.text)
    except Exception as e:
        print(f"❌ TXT upload error: {e}")

def test_invalid_file():
    """Test invalid file upload"""
    print("\n🚫 Testing invalid file upload...")
    try:
        files = {"file": ("test.docx", b"invalid content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code == 400:
            print("✅ Invalid file correctly rejected:", response.json())
        else:
            print("❌ Invalid file should have been rejected:", response.status_code, response.text)
    except Exception as e:
        print(f"❌ Invalid file test error: {e}")

def main():
    """Run all manual tests"""
    print("🚀 Starting manual API tests...")
    print(f"📍 Testing against: {BASE_URL}")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ Service is not running. Please start it first:")
        print("   source renv/bin/activate")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Run other tests
    test_upload_pdf()
    test_upload_txt()
    test_invalid_file()
    
    print("\n" + "=" * 50)
    print("✨ Manual tests completed!")

if __name__ == "__main__":
    main()
