#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_status "Docker is running"
}

# Function to create Docker volumes
create_volumes() {
    print_status "Creating Docker volumes..."
    
    if ! docker volume ls -q | grep -q "^qdrant_data$"; then
        docker volume create qdrant_data
        print_success "Created volume: qdrant_data"
    else
        print_status "Volume qdrant_data already exists"
    fi
    
    if ! docker volume ls -q | grep -q "^redis_data$"; then
        docker volume create redis_data
        print_success "Created volume: redis_data"
    else
        print_status "Volume redis_data already exists"
    fi
}

# Function to launch Qdrant
launch_qdrant() {
    print_status "Starting Qdrant container..."
    
    docker run -d \
        --name qdrant \
        -p 6333:6333 \
        -p 6334:6334 \
        -v qdrant_data:/qdrant/storage \
        -e QDRANT__SERVICE__HTTP_PORT=6333 \
        -e QDRANT__SERVICE__GRPC_PORT=6334 \
        --restart unless-stopped \
        qdrant/qdrant:latest
    
    if [ $? -eq 0 ]; then
        print_success "Qdrant container started successfully"
    else
        print_error "Failed to start Qdrant container"
        exit 1
    fi
}

# Function to launch Redis
launch_redis() {
    print_status "Starting Redis container..."
    
    docker run -d \
        --name redis \
        -p 6379:6379 \
        -v redis_data:/data \
        --restart unless-stopped \
        redis:7-alpine \
        redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    
    if [ $? -eq 0 ]; then
        print_success "Redis container started successfully"
    else
        print_error "Failed to start Redis container"
        exit 1
    fi
}

# Function to check container health
check_health() {
    local container_name=$1
    local max_retries=10
    local retry_count=0
    
    print_status "Checking health of $container_name..."
    
    while [ $retry_count -lt $max_retries ]; do
        if docker inspect --format "{{.State.Health.Status}}" $container_name 2>/dev/null | grep -q "healthy"; then
            print_success "$container_name is healthy"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        print_status "Waiting for $container_name to become healthy... ($retry_count/$max_retries)"
        sleep 5
    done
    
    print_warning "$container_name health check timed out. Check logs for details."
    return 1
}

# Function to show logs
show_logs() {
    print_status "Showing logs for all containers. Press Ctrl+C to stop..."
    echo "=============================================================="
    
    # Show logs for both containers with colored output
    docker logs -f qdrant & 
    QDRANT_PID=$!
    
    docker logs -f redis &
    REDIS_PID=$!
    
    # Wait for user interrupt
    trap 'kill $QDRANT_PID $REDIS_PID 2>/dev/null; exit 0' INT
    wait
}

# Function to cleanup on script exit
cleanup() {
    print_status "Cleaning up..."
    kill $QDRANT_PID $REDIS_PID 2>/dev/null
}

# Main execution
main() {
    print_status "Starting Docker containers setup..."
    
    # Check Docker
    check_docker
    
    # Remove existing containers if they exist
    print_status "Removing existing containers if they exist..."
    docker rm -f qdrant redis 2>/dev/null
    
    # Create volumes
    create_volumes
    
    # Launch containers
    launch_qdrant
    launch_redis
    
    # Wait a bit for containers to start
    sleep 3
    
    # Check health
    check_health qdrant
    check_health redis
    
    # Display container information
    echo ""
    print_success "Containers started successfully!"
    echo "=============================================================="
    print_status "Qdrant:"
    echo "  - HTTP API: http://localhost:6333"
    echo "  - gRPC API: localhost:6334"
    echo "  - Health: http://localhost:6333/health"
    echo ""
    print_status "Redis:"
    echo "  - Port: localhost:6379"
    echo "  - Max Memory: 512MB"
    echo "  - Memory Policy: allkeys-lru"
    echo "=============================================================="
    echo ""
    
    # Ask user if they want to see logs
    read -p "Do you want to view container logs? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        show_logs
    else
        print_status "You can view logs later using:"
        echo "  docker logs -f qdrant"
        echo "  docker logs -f redis"
        echo ""
        print_status "To stop containers:"
        echo "  docker stop qdrant redis"
        echo "  docker rm qdrant redis"
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"