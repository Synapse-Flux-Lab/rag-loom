# Testing Guide for RAG Platform Kit

This directory contains comprehensive tests for the RAG platform kit.

## Directory Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API endpoints
├── samples/        # Sample test scripts and data
├── conftest.py     # Pytest configuration and fixtures
└── requirements-test.txt  # Test dependencies
```

## Quick Start

### 1. Install Test Dependencies
```bash
source renv/bin/activate
pip install -r tests/requirements-test.txt
```

### 2. Run All Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
```

### 3. Manual Testing
```bash
# Start the service locally
source renv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, run manual tests
python tests/samples/test_manual.py
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **FileProcessor**: Tests for text extraction, cleaning, and file type detection
- **Chunking**: Tests for text chunking algorithms
- **Config**: Tests for configuration management

### Integration Tests (`tests/integration/`)
- **API Endpoints**: Tests for file upload, processing, and retrieval
- **End-to-End**: Tests for complete workflows

### Manual Tests (`tests/samples/`)
- **API Testing**: Scripts for testing the running service
- **Sample Data**: Test files and content for various scenarios

## Running Tests in Different Environments

### Local Development
```bash
pytest -v --tb=short
```

### CI/CD Pipeline
```bash
pytest --cov=app --cov-report=xml --junitxml=test-results.xml
```

### Debug Mode
```bash
pytest -v -s --pdb
```

## Test Data

The tests use sample data including:
- **Sample PDF**: Minimal PDF with "Hello World" text
- **Sample TXT**: Simple text file for testing
- **Invalid Files**: Files that should be rejected

## Coverage Reports

After running tests with coverage, view the HTML report:
```bash
open htmlcov/index.html
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure you're in the virtual environment
2. **Connection Errors**: Make sure the service is running for integration tests
3. **Missing Dependencies**: Install test requirements

### Debug Commands
```bash
# Check what's installed
pip list | grep pytest

# Run single test
pytest tests/unit/test_file_processing.py::TestFileProcessor::test_extract_text_from_txt

# Run with verbose output
pytest -vvv
```
