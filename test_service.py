#!/usr/bin/env python3
"""
Simple test script to verify the RAG service is working
Run this after starting your service locally
"""

import requests
import time

def test_service():
    """Test if the service is running and responding"""
    base_url = "http://localhost:8000"
    
    print("🚀 Testing RAG Service...")
    print(f"📍 Service URL: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
        else:
            print("❌ Health check failed:", response.status_code, response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to service!")
        print("💡 Make sure the service is running:")
        print("   source renv/bin/activate")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Check available endpoints
    print("\n📋 Checking available endpoints...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation available at /docs")
        else:
            print("⚠️  API docs not available (this is okay)")
    except Exception as e:
        print(f"⚠️  Could not check API docs: {e}")
    
    print("\n" + "=" * 50)
    print("✨ Service test completed successfully!")
    print("🌐 You can now:")
    print("   - View API docs: http://localhost:8000/docs")
    print("   - Test endpoints: http://localhost:8000/health")
    print("   - Run full tests: python -m pytest")
    print("   - Run manual tests: python tests/samples/test_manual.py")
    
    return True

if __name__ == "__main__":
    test_service()
