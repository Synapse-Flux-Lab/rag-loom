#!/bin/bash

# RAG Platform Kit - Quick Start Script
# This script helps you quickly set up and test the RAG service

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_PORT=8000
SERVICE_URL="http://localhost:$SERVICE_PORT"
VENV_NAME="renv"

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python3 found: $PYTHON_VERSION"
    else
        print_error "Python3 not found. Please install Python 3.9+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        print_error "pip3 not found. Please install pip"
        exit 1
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        print_success "git found"
    else
        print_warning "git not found (optional for development)"
    fi
}

setup_virtual_environment() {
    print_header "Setting Up Virtual Environment"
    
    if [ -d "$VENV_NAME" ]; then
        print_info "Virtual environment already exists"
    else
        print_info "Creating virtual environment..."
        python3 -m venv $VENV_NAME
        print_success "Virtual environment created"
    fi
    
    print_info "Activating virtual environment..."
    source $VENV_NAME/bin/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip
    print_success "Virtual environment ready"
}

install_dependencies() {
    print_header "Installing Dependencies"
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

check_service_status() {
    print_header "Checking Service Status"
    
    if curl -s "$SERVICE_URL/health" > /dev/null 2>&1; then
        print_success "Service is running on port $SERVICE_PORT"
        return 0
    else
        print_warning "Service is not running on port $SERVICE_PORT"
        return 1
    fi
}

start_service() {
    print_header "Starting RAG Service"
    
    if check_service_status; then
        print_info "Service is already running"
        return 0
    fi
    
    print_info "Starting service in background..."
    
    # Start service in background
    nohup uvicorn app.main:app --host 0.0.0.0 --port $SERVICE_PORT --reload > service.log 2>&1 &
    SERVICE_PID=$!
    
    # Wait for service to start
    print_info "Waiting for service to start..."
    for i in {1..30}; do
        if check_service_status; then
            print_success "Service started successfully (PID: $SERVICE_PID)"
            echo $SERVICE_PID > service.pid
            return 0
        fi
        sleep 1
    done
    
    print_error "Service failed to start within 30 seconds"
    return 1
}

stop_service() {
    print_header "Stopping RAG Service"
    
    if [ -f "service.pid" ]; then
        SERVICE_PID=$(cat service.pid)
        if kill -0 $SERVICE_PID 2>/dev/null; then
            print_info "Stopping service (PID: $SERVICE_PID)..."
            kill $SERVICE_PID
            rm -f service.pid
            print_success "Service stopped"
        else
            print_warning "Service PID not found, cleaning up..."
            rm -f service.pid
        fi
    else
        print_warning "No service PID file found"
    fi
}

run_tests() {
    print_header "Running API Tests"
    
    if ! check_service_status; then
        print_error "Service is not running. Please start it first."
        return 1
    fi
    
    if [ -f "docs/test_api.py" ]; then
        print_info "Running comprehensive API tests..."
        python docs/test_api.py
        return $?
    else
        print_warning "Test script not found at docs/test_api.py"
        return 1
    fi
}

show_service_info() {
    print_header "Service Information"
    
    if check_service_status; then
        print_success "Service Status: Running"
        print_info "Service URL: $SERVICE_URL"
        print_info "Health Check: $SERVICE_URL/health"
        print_info "API Docs: $SERVICE_URL/docs"
        print_info "OpenAPI: $SERVICE_URL/openapi.json"
        
        # Show health details
        echo ""
        print_info "Health Details:"
        curl -s "$SERVICE_URL/health" | python3 -m json.tool 2>/dev/null || echo "Could not parse health response"
    else
        print_error "Service Status: Not Running"
        print_info "To start the service, run: ./docs/quick_start.sh start"
    fi
}

show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Set up virtual environment and install dependencies"
    echo "  start     - Start the RAG service"
    echo "  stop      - Stop the RAG service"
    echo "  restart   - Restart the RAG service"
    echo "  status    - Show service status and information"
    echo "  test      - Run API tests"
    echo "  logs      - Show service logs"
    echo "  clean     - Clean up service files"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup      # Initial setup"
    echo "  $0 start      # Start service"
    echo "  $0 test       # Run tests"
    echo "  $0 status     # Check status"
}

show_logs() {
    print_header "Service Logs"
    
    if [ -f "service.log" ]; then
        tail -n 50 service.log
    else
        print_warning "No service logs found"
    fi
}

cleanup() {
    print_header "Cleaning Up"
    
    stop_service
    rm -f service.log service.pid
    
    print_success "Cleanup completed"
}

# Main script logic
case "${1:-help}" in
    setup)
        check_prerequisites
        setup_virtual_environment
        install_dependencies
        print_success "Setup completed successfully!"
        print_info "Next steps:"
        print_info "  1. Configure your .env file with API keys"
        print_info "  2. Run: $0 start"
        print_info "  3. Run: $0 test"
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    status)
        show_service_info
        ;;
    test)
        run_tests
        ;;
    logs)
        show_logs
        ;;
    clean)
        cleanup
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
