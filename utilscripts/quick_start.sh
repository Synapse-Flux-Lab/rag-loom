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

# Function to check if service is running
is_service_running() {
    if curl -s "$SERVICE_URL/health" > /dev/null 2>&1; then
        return 0
    else
        # Also check if process is running by port
        if lsof -ti:$SERVICE_PORT > /dev/null 2>&1; then
            return 0
        fi
        return 1
    fi
}

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
    echo " Setting up virtual environment..."
    
    # Check if Python 3.12 is available
    if ! command -v python3.12 &> /dev/null; then
        echo "❌ Python 3.12 not found. Installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if ! command -v brew &> /dev/null; then
                echo "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python@3.12
        else
            echo "Please install Python 3.12 manually for your OS"
            return 1
        fi
    fi
    
    # Check if venv already exists
    if [ -d "venvpy312" ]; then
        echo "⚠️  Virtual environment 'venvpy312' already exists!"
        echo "   If you want to recreate it, manually remove it first:"
        echo "   rm -rf venvpy312"
        echo "   Then run this setup command again."
        echo ""
        echo "   Or continue using the existing venv by running:"
        echo "   ./quick_start.sh start"
        return 0
    fi
    
    # Create new venv with Python 3.12 explicitly
    echo "📦 Creating virtual environment with Python 3.12..."
    python3.12 -m venv venvpy312
    
    # Activate the venv
    source venvpy312/bin/activate
    
    # Verify Python version
    PYTHON_VERSION=$(python --version 2>&1)
    echo "✅ Virtual environment created with: $PYTHON_VERSION"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    if pip install --upgrade -r requirements.txt; then
        echo "✅ Dependencies installed successfully!"
    else
        echo "❌ Failed to install dependencies. Check the error above."
        return 1
    fi
}

install_dependencies() {
    print_header "Installing Dependencies"
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    print_info "Installing Python dependencies..."
    pip install --upgrade -r requirements.txt
    print_success "Dependencies installed"
}

check_service_status() {
    print_header "Checking Service Status"
    
    if is_service_running; then
        print_success "Service is running on port $SERVICE_PORT"
        return 0
    else
        print_warning "Service is not running on port $SERVICE_PORT"
        return 1
    fi
}

start_service() {
    echo "🚀 Starting RAG service..."
    
    # Activate virtual environment
    if ! activate_virtual_environment; then
        return 1
    fi
    
    # Check if service is already running
    if is_service_running; then
        echo "⚠️  Service is already running on port $SERVICE_PORT"
        return 0
    fi
    
    # Start the service
    echo "📡 Starting service on port $SERVICE_PORT..."
    nohup uvicorn app.main:app --host 0.0.0.0 --port $SERVICE_PORT --reload > service.log 2>&1 &
    
    # Save the PID
    echo $! > service.pid
    echo "📋 Service started with PID: $(cat service.pid)"
    
    # Wait a moment for service to start
    sleep 3
    
    if is_service_running; then
        echo "✅ Service started successfully on port $SERVICE_PORT"
        echo " Service logs: tail -f service.log"
    else
        echo "❌ Failed to start service. Check logs: cat service.log"
        rm -f service.pid
        return 1
    fi
}

stop_service() {
    echo "========================================"
    echo "  Stopping RAG Service"
    echo "========================================"
    
    # Check if service is running by port
    if is_service_running; then
        echo " Service is running on port $SERVICE_PORT. Stopping..."
        
        # Try to stop using PID file first
        if [ -f "service.pid" ]; then
            PID=$(cat service.pid)
            if kill -0 $PID 2>/dev/null; then
                echo "📋 Stopping service with PID: $PID"
                kill $PID
                sleep 2
                if kill -0 $PID 2>/dev/null; then
                    echo "⚠️  Service didn't stop gracefully, force killing..."
                    kill -9 $PID
                fi
            fi
            rm -f service.pid
        else
            echo "⚠️  No PID file found, stopping by port..."
        fi
        
        # Force stop any process using the port
        PORT_PIDS=$(lsof -ti:$SERVICE_PORT 2>/dev/null || true)
        if [ ! -z "$PORT_PIDS" ]; then
            echo "🔍 Found processes using port $SERVICE_PORT: $PORT_PIDS"
            echo "🛑 Stopping all processes on port $SERVICE_PORT..."
            echo "$PORT_PIDS" | xargs kill -9 2>/dev/null || true
            sleep 1
        fi
        
        # Verify service is stopped
        if is_service_running; then
            echo "❌ Failed to stop service. Manual intervention may be required."
            echo "   Try: sudo lsof -ti:$SERVICE_PORT | xargs sudo kill -9"
            return 1
        else
            echo "✅ Service stopped successfully"
        fi
    else
        echo "ℹ️  No service running on port $SERVICE_PORT"
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
        print_info "To start the service, run: ./utilscripts/quick_start.sh start"
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

activate_virtual_environment() {
    if [ -d "venvpy312" ]; then
        echo " Activating virtual environment..."
        source venvpy312/bin/activate
        
        # Verify Python version
        PYTHON_VERSION=$(python --version 2>&1)
        if [[ $PYTHON_VERSION == *"3.12"* ]]; then
            echo "✅ Virtual environment activated with Python 3.12"
            return 0
        else
            echo "❌ Warning: Virtual environment is not using Python 3.12"
            echo "Current version: $PYTHON_VERSION"
            echo "Consider recreating the venv: rm -rf venvpy312 && ./quick_start.sh setup"
            return 1
        fi
    else
        echo "❌ Virtual environment not found. Run setup first:"
        echo "   ./quick_start.sh setup"
        return 1
    fi
}

cleanup_orphaned_processes() {
    echo " Cleaning up orphaned processes..."
    
    # Find any Python processes that might be our service
    PYTHON_PIDS=$(ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}' 2>/dev/null || true)
    
    if [ ! -z "$PYTHON_PIDS" ]; then
        echo "🔍 Found orphaned uvicorn processes: $PYTHON_PIDS"
        echo "🛑 Stopping orphaned processes..."
        echo "$PYTHON_PIDS" | xargs kill -9 2>/dev/null || true
        echo "✅ Cleanup completed"
    else
        echo "ℹ️  No orphaned processes found"
    fi
    
    # Remove stale PID file if it exists
    if [ -f "service.pid" ]; then
        PID=$(cat service.pid)
        if ! kill -0 $PID 2>/dev/null; then
            echo "🗑️  Removing stale PID file"
            rm -f service.pid
        fi
    fi
}

# Main script logic
case "${1:-help}" in
    setup)
        check_prerequisites
        setup_virtual_environment
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
    cleanup)
        cleanup_orphaned_processes
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