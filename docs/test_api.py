#!/usr/bin/env python3
"""
Comprehensive API Testing Script for RAG Platform Kit
This script tests all endpoints with sample data and provides detailed feedback.

Usage:
    python docs/test_api.py

Prerequisites:
    1. Start the RAG service: uvicorn app.main:app --host 0.0.0.0 --port 8000
    2. Install requests: pip install requests
"""

import requests
import json
import time
import os
from typing import Dict, Any, List
from datetime import datetime

class RAGAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Sample data for testing
        self.sample_data = self._create_sample_data()
        
        # Test results
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def _create_sample_data(self) -> Dict[str, Any]:
        """Create sample data for testing"""
        return {
            'sample_text': "This is a sample text document for testing the RAG platform. "
                          "It contains information about machine learning, artificial intelligence, "
                          "and natural language processing. Machine learning is a subset of AI that "
                          "enables computers to learn from data without being explicitly programmed. "
                          "Natural language processing helps computers understand and generate human language.",
            
            'sample_pdf_content': b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
                                 b"2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n"
                                 b"3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n"
                                 b"/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\n"
                                 b"BT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\n"
                                 b"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n"
                                 b"0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\n"
                                 b"startxref\n297\n%%EOF",
            
            'search_queries': [
                "What is machine learning?",
                "Explain artificial intelligence",
                "How does natural language processing work?",
                "What are the benefits of AI?",
                "Describe deep learning techniques"
            ],
            
            'generation_queries': [
                "Explain the relationship between machine learning and AI",
                "What are the main applications of natural language processing?",
                "How can machine learning improve business processes?",
                "Describe the future of artificial intelligence"
            ]
        }
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"🔍 {title}")
        print("="*60)
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result with formatting"""
        if success:
            print(f"✅ {test_name}: PASSED")
            self.results['passed'] += 1
        else:
            print(f"❌ {test_name}: FAILED")
            self.results['failed'] += 1
            if details:
                print(f"   Details: {details}")
    
    def test_health_endpoint(self) -> bool:
        """Test the health check endpoint"""
        self.print_header("Testing Health Endpoint")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check successful")
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Vector Store: {data.get('vector_store', 'N/A')}")
                print(f"   Embedding Model: {data.get('embedding_model', 'N/A')}")
                print(f"   LLM Provider: {data.get('llm_provider', 'N/A')}")
                return True
            else:
                self.print_result("Health Check", False, f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.print_result("Health Check", False, "Could not connect to service")
            return False
        except Exception as e:
            self.print_result("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint"""
        self.print_header("Testing Root Endpoint")
        
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint successful")
                print(f"   Message: {data.get('message', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
                return True
            else:
                self.print_result("Root Endpoint", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("Root Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_ingestion_endpoint(self) -> bool:
        """Test the document ingestion endpoint"""
        self.print_header("Testing Document Ingestion")
        
        try:
            # Test with text file
            files = {
                'file': ('sample.txt', self.sample_data['sample_text'], 'text/plain')
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ingest",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Text ingestion successful")
                print(f"   File ID: {data.get('file_id', 'N/A')}")
                print(f"   Chunks Created: {data.get('chunks_created', 'N/A')}")
                print(f"   Processing Time: {data.get('processing_time', 'N/A')}s")
                return True
            else:
                self.print_result("Text Ingestion", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            self.print_result("Text Ingestion", False, f"Error: {str(e)}")
            return False
    
    def test_batch_ingestion_endpoint(self) -> bool:
        """Test the batch ingestion endpoint"""
        self.print_header("Testing Batch Ingestion")
        
        try:
            # Test with multiple text files
            files = [
                ('files', ('doc1.txt', self.sample_data['sample_text'], 'text/plain')),
                ('files', ('doc2.txt', self.sample_data['sample_text'], 'text/plain'))
            ]
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ingest/batch",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Batch ingestion successful")
                print(f"   Files Processed: {len(data)}")
                for i, result in enumerate(data):
                    print(f"   File {i+1}: {result.get('file_id', 'N/A')} - {result.get('chunks_created', 'N/A')} chunks")
                return True
            else:
                self.print_result("Batch Ingestion", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            self.print_result("Batch Ingestion", False, f"Error: {str(e)}")
            return False
    
    def test_search_endpoint(self) -> bool:
        """Test the document search endpoint"""
        self.print_header("Testing Document Search")
        
        try:
            # Test search with different queries
            for i, query in enumerate(self.sample_data['search_queries'][:3]):
                payload = {
                    "query": query,
                    "top_k": 3,
                    "similarity_threshold": 0.5
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/search",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Search query {i+1} successful: '{query[:50]}...'")
                    print(f"   Results returned: {len(data)}")
                else:
                    print(f"❌ Search query {i+1} failed: '{query[:50]}...'")
                    print(f"   Status code: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                
                time.sleep(0.5)  # Small delay between requests
            
            return True
                
        except Exception as e:
            self.print_result("Document Search", False, f"Error: {str(e)}")
            return False
    
    def test_generation_endpoint(self) -> bool:
        """Test the answer generation endpoint"""
        self.print_header("Testing Answer Generation")
        
        try:
            # Test generation with different queries
            for i, query in enumerate(self.sample_data['generation_queries'][:2]):
                payload = {
                    "query": query,
                    "search_params": {
                        "query": query,
                        "top_k": 2,
                        "similarity_threshold": 0.5
                    },
                    "temperature": 0.7,
                    "max_tokens": 300
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Generation query {i+1} successful: '{query[:50]}...'")
                    print(f"   Answer length: {len(data.get('answer', ''))} characters")
                    print(f"   Generation time: {data.get('generation_time', 'N/A')}s")
                    print(f"   Sources: {len(data.get('sources', []))}")
                else:
                    print(f"❌ Generation query {i+1} failed: '{query[:50]}...'")
                    print(f"   Status code: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                
                time.sleep(1)  # Delay between requests
            
            return True
                
        except Exception as e:
            self.print_result("Answer Generation", False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling for invalid requests"""
        self.print_header("Testing Error Handling")
        
        try:
            # Test invalid file type
            files = {
                'file': ('invalid.docx', b'invalid content', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/ingest",
                files=files
            )
            
            if response.status_code == 400:
                print(f"✅ Invalid file type correctly rejected")
            else:
                print(f"❌ Invalid file type should have been rejected (status: {response.status_code})")
                return False
            
            # Test invalid search query
            payload = {"invalid_field": "test"}
            response = self.session.post(
                f"{self.base_url}/api/v1/search",
                json=payload
            )
            
            if response.status_code in [400, 422]:
                print(f"✅ Invalid search query correctly rejected")
            else:
                print(f"❌ Invalid search query should have been rejected (status: {response.status_code})")
                return False
            
            return True
                
        except Exception as e:
            self.print_result("Error Handling", False, f"Error: {str(e)}")
            return False
    
    def test_api_documentation(self) -> bool:
        """Test if API documentation is accessible"""
        self.print_header("Testing API Documentation")
        
        try:
            # Test OpenAPI schema
            response = self.session.get(f"{self.base_url}/openapi.json")
            if response.status_code == 200:
                print(f"✅ OpenAPI schema accessible")
            else:
                print(f"❌ OpenAPI schema not accessible (status: {response.status_code})")
                return False
            
            # Test Swagger UI
            response = self.session.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                print(f"✅ Swagger UI accessible")
            else:
                print(f"❌ Swagger UI not accessible (status: {response.status_code})")
                return False
            
            return True
                
        except Exception as e:
            self.print_result("API Documentation", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all API tests"""
        print("🚀 Starting Comprehensive API Testing")
        print(f"📍 Testing against: {self.base_url}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("Root Endpoint", self.test_root_endpoint),
            ("Document Ingestion", self.test_ingestion_endpoint),
            ("Batch Ingestion", self.test_batch_ingestion_endpoint),
            ("Document Search", self.test_search_endpoint),
            ("Answer Generation", self.test_generation_endpoint),
            ("Error Handling", self.test_error_handling),
            ("API Documentation", self.test_api_documentation)
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.results['errors'].append(f"{test_name}: {str(e)}")
                self.results['failed'] += 1
        
        return self.results
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total_tests = self.results['passed'] + self.results['failed']
        success_rate = (self.results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Test Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {self.results['passed']} ✅")
        print(f"   Failed: {self.results['failed']} ❌")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if self.results['errors']:
            print(f"\n❌ Errors encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")
        
        if success_rate == 100:
            print(f"\n🎉 All tests passed! Your RAG API is working perfectly!")
        elif success_rate >= 80:
            print(f"\n👍 Most tests passed. Check the failed tests above.")
        else:
            print(f"\n⚠️  Many tests failed. Please check your service configuration.")

def main():
    """Main function to run the API tests"""
    print("🔍 RAG Platform Kit - API Testing Suite")
    print("=" * 60)
    
    # Check if service is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Service is not responding properly")
            print("💡 Please ensure the service is running:")
            print("   source renv/bin/activate")
            print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to service")
        print("💡 Please start the service first:")
        print("   source renv/bin/activate")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Run tests
    tester = RAGAPITester()
    results = tester.run_all_tests()
    
    # Print summary
    tester.print_summary()
    
    # Exit with appropriate code
    if results['failed'] == 0:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
