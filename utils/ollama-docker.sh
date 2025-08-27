#!/bin/bash

# Ollama Docker Manager Script
# This script manages Ollama running in a Docker container

set -e  # Exit on any error

CONTAINER_NAME="ollama"
IMAGE_NAME="ollama/ollama"
MODEL_NAME="gemma2:2b"
PORT="11434"

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Docker is not running. Starting Docker..."
        # Try to start Docker (method depends on your OS and Docker installation)
        if command -v docker > /dev/null 2>&1; then
            open -a Docker || sudo systemctl start docker || sudo service docker start
            # Wait for Docker to start
            sleep 30
        else
            echo "Docker is not installed. Please install Docker first."
            exit 1
        fi
    fi
}

# Function to check if container exists
container_exists() {
    docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Function to check if container is running
container_running() {
    docker ps --filter "name=^/${CONTAINER_NAME}$" --filter "status=running" --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"
}

# Function to start container
start_container() {
    echo "Starting Ollama container..."
    docker start $CONTAINER_NAME
    
    # Wait for container to be ready
    echo "Waiting for Ollama to start..."
    sleep 10
    
    # Check if Ollama is responding
    local max_attempts=10
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker exec $CONTAINER_NAME curl -s http://localhost:11434 > /dev/null; then
            echo "Ollama is running and ready!"
            return 0
        fi
        echo "Waiting for Ollama to be ready (attempt $attempt/$max_attempts)..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "Failed to start Ollama after $max_attempts attempts"
    return 1
}

# Function to create and run new container
create_container() {
    echo "Creating new Ollama container..."
    docker run -d \
        -v ollama:/root/.ollama \
        -p $PORT:11434 \
        --name $CONTAINER_NAME \
        $IMAGE_NAME
    
    # Wait for container to be ready
    echo "Waiting for Ollama to start..."
    sleep 15
    
    # Check if Ollama is responding
    local max_attempts=10
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker exec $CONTAINER_NAME curl -s http://localhost:11434 > /dev/null; then
            echo "Ollama is running and ready!"
            return 0
        fi
        echo "Waiting for Ollama to be ready (attempt $attempt/$max_attempts)..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "Failed to start Ollama after $max_attempts attempts"
    return 1
}

# Function to pull model
pull_model() {
    echo "Pulling model $MODEL_NAME..."
    docker exec $CONTAINER_NAME ollama pull $MODEL_NAME
    
    # Verify model was pulled successfully
    if docker exec $CONTAINER_NAME ollama list | grep -q "$MODEL_NAME"; then
        echo "Model $MODEL_NAME pulled successfully!"
    else
        echo "Failed to pull model $MODEL_NAME"
        return 1
    fi
}

# Function to check if model exists
model_exists() {
    docker exec $CONTAINER_NAME ollama list | grep -q "$MODEL_NAME"
}

# Main execution
echo "=== Ollama Docker Manager ==="
check_docker

if container_exists; then
    echo "Container '$CONTAINER_NAME' exists."
    
    if container_running; then
        echo "Container is already running."
    else
        start_container
    fi
else
    create_container
fi

# Check if model exists, pull if not
if model_exists; then
    echo "Model $MODEL_NAME already exists."
else
    pull_model
fi

echo "=== Setup Complete ==="
echo "Ollama is running at: http://localhost:$PORT"
echo "Test with: docker exec $CONTAINER_NAME ollama run $MODEL_NAME 'Hello'"