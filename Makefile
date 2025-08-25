# =============================================================================
# RAG Platform Kit - Development Makefile
# =============================================================================

.PHONY: help install install-dev install-test install-docs clean test test-unit test-integration test-e2e lint format type-check security-check coverage docker-build docker-run docker-stop docker-clean ci-cd-local pre-commit-install pre-commit-run docs-build docs-serve

# Default target
help:
	@echo "🚀 RAG Platform Kit - Development Commands"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  install-test     Install testing dependencies"
	@echo "  install-docs     Install documentation dependencies"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-e2e         Run end-to-end tests only"
	@echo "  coverage         Generate coverage report"
	@echo ""
	@echo "🔍 Code Quality:"
	@echo "  lint             Run all linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo "  security-check   Run security scans"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run Docker container"
	@echo "  docker-stop      Stop Docker container"
	@echo "  docker-clean     Clean Docker resources"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs-build       Build documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "🔄 CI/CD:"
	@echo "  ci-cd-local      Run CI/CD pipeline locally"
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo "  pre-commit-run   Run pre-commit hooks"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean            Clean build artifacts and cache"

# =============================================================================
# INSTALLATION
# =============================================================================

install:
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "🔧 Installing development dependencies..."
	pip install -e ".[dev]"

install-test:
	@echo "🧪 Installing testing dependencies..."
	pip install -e ".[test]"

install-docs:
	@echo "📚 Installing documentation dependencies..."
	pip install -e ".[docs]"

# =============================================================================
# TESTING
# =============================================================================

test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v --cov=app --cov-report=term-missing

test-integration:
	@echo "🔗 Running integration tests..."
	pytest tests/integration/ -v --cov=app --cov-report=term-missing

test-e2e:
	@echo "🌐 Running end-to-end tests..."
	pytest tests/e2e/ -v --cov=app --cov-report=term-missing

coverage:
	@echo "📊 Generating coverage report..."
	pytest tests/ --cov=app --cov-report=html --cov-report=xml
	@echo "📁 Coverage report generated in htmlcov/"

# =============================================================================
# CODE QUALITY
# =============================================================================

lint:
	@echo "🔍 Running linting checks..."
	flake8 app/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	black --check --diff app/ tests/
	isort --check-only --diff app/ tests/

format:
	@echo "🎨 Formatting code..."
	black app/ tests/
	isort app/ tests/

type-check:
	@echo "🔍 Running type checking..."
	mypy app/ --ignore-missing-imports --no-strict-optional

security-check:
	@echo "🔒 Running security checks..."
	bandit -r app/ -f json -o bandit-report.json || true
	safety check --json --output safety-report.json || true
	@echo "📁 Security reports generated: bandit-report.json, safety-report.json"

# =============================================================================
# DOCKER
# =============================================================================

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t rag-platform-kit:latest .

docker-run:
	@echo "🚀 Running Docker container..."
	docker run -d --name rag-service \
		-p 8000:8000 \
		-e LLM_PROVIDER=huggingface \
		-e VECTOR_STORE_TYPE=chroma \
		rag-platform-kit:latest

docker-stop:
	@echo "🛑 Stopping Docker container..."
	docker stop rag-service || true
	docker rm rag-service || true

docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker system prune -f
	docker image prune -f

# =============================================================================
# DOCUMENTATION
# =============================================================================

docs-build:
	@echo "📚 Building documentation..."
	mkdocs build

docs-serve:
	@echo "🌐 Serving documentation locally..."
	mkdocs serve

# =============================================================================
# CI/CD
# =============================================================================

ci-cd-local:
	@echo "🔄 Running CI/CD pipeline locally..."
	@echo "1. Code quality checks..."
	$(MAKE) lint
	@echo "2. Type checking..."
	$(MAKE) type-check
	@echo "3. Security checks..."
	$(MAKE) security-check
	@echo "4. Running tests..."
	$(MAKE) test
	@echo "5. Building Docker image..."
	$(MAKE) docker-build
	@echo "✅ CI/CD pipeline completed successfully!"

pre-commit-install:
	@echo "🔧 Installing pre-commit hooks..."
	pre-commit install
	pre-commit install --hook-type commit-msg

pre-commit-run:
	@echo "🔍 Running pre-commit hooks..."
	pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

clean:
	@echo "🧹 Cleaning build artifacts and cache..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type f -name "*.log" -delete
	@echo "🧹 Cleanup completed!"

# =============================================================================
# DEVELOPMENT SERVER
# =============================================================================

dev-server:
	@echo "🚀 Starting development server..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# =============================================================================
# PRODUCTION
# =============================================================================

prod-start:
	@echo "🚀 Starting production services..."
	./start_production.sh

prod-stop:
	@echo "🛑 Stopping production services..."
	docker-compose down

prod-logs:
	@echo "📋 Showing production logs..."
	docker-compose logs -f

prod-status:
	@echo "📊 Production service status..."
	docker-compose ps

# =============================================================================
# MONITORING
# =============================================================================

monitor-start:
	@echo "📊 Starting monitoring services..."
	docker-compose up -d prometheus grafana

monitor-stop:
	@echo "🛑 Stopping monitoring services..."
	docker-compose stop prometheus grafana

monitor-logs:
	@echo "📋 Showing monitoring logs..."
	docker-compose logs -f prometheus grafana

# =============================================================================
# UTILITIES
# =============================================================================

check-deps:
	@echo "🔍 Checking dependency conflicts..."
	pip check

update-deps:
	@echo "🔄 Updating dependencies..."
	pip install --upgrade -r requirements.txt

freeze-deps:
	@echo "📋 Freezing current dependencies..."
	pip freeze > requirements.frozen.txt

venv-create:
	@echo "🏗️ Creating virtual environment..."
	python3.12 -m venv venv
	@echo "✅ Virtual environment created. Activate with: source venv/bin/activate"

venv-activate:
	@echo "🔧 Activating virtual environment..."
	@echo "Run: source venv/bin/activate"

# =============================================================================
# QUICK COMMANDS
# =============================================================================

quick-test:
	@echo "⚡ Quick test run..."
	pytest tests/ -x --tb=short

quick-lint:
	@echo "⚡ Quick lint check..."
	black --check app/ && isort --check-only app/

quick-format:
	@echo "⚡ Quick format..."
	black app/ && isort app/

# =============================================================================
# HELPERS
# =============================================================================

show-env:
	@echo "🌍 Environment information:"
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Current directory: $(shell pwd)"
	@echo "Virtual environment: $(shell echo $$VIRTUAL_ENV)"

show-deps:
	@echo "📦 Installed packages:"
	@pip list

show-test-results:
	@echo "📊 Test results:"
	@if [ -f "test-results.xml" ]; then echo "✅ Test results available"; else echo "❌ No test results found"; fi
	@if [ -d "htmlcov" ]; then echo "✅ Coverage report available"; else echo "❌ No coverage report found"; fi
