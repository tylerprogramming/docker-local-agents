#!/bin/bash

# Function to check if Ollama container is running
check_ollama() {
    if ! docker ps | grep -q ollama; then
        echo "❌ Ollama container is not running. Please start it first with 'docker-compose up -d ollama'"
        exit 1
    fi
}

# Function to wait for Ollama to be ready
wait_for_ollama() {
    echo "Waiting for Ollama to be ready..."
    while ! docker exec ollama curl -s http://localhost:11434/api/tags > /dev/null; do
        echo "Waiting for Ollama server..."
        sleep 2
    done
    echo "✅ Ollama is ready!"
}

# Function to list all models
list_models() {
    echo "📋 Listing all models..."
    docker exec -it ollama ollama list
}

# Function to pull a model
pull_model() {
    if [ -z "$1" ]; then
        echo "❌ Please specify a model name"
        echo "Usage: ./ollama-commands.sh pull <model-name>"
        echo "Example: ./ollama-commands.sh pull qwen3:1.7b"
        exit 1
    fi
    echo "📥 Pulling model $1..."
    docker exec -it ollama ollama pull $1
}

# Function to run a model interactively
run_model() {
    if [ -z "$1" ]; then
        echo "❌ Please specify a model name"
        echo "Usage: ./ollama-commands.sh run <model-name>"
        echo "Example: ./ollama-commands.sh run qwen3:1.7b"
        exit 1
    fi
    echo "🤖 Running model $1 interactively..."
    docker exec -it ollama ollama run $1
}

# Function to remove a model
remove_model() {
    if [ -z "$1" ]; then
        echo "❌ Please specify a model name"
        echo "Usage: ./ollama-commands.sh remove <model-name>"
        echo "Example: ./ollama-commands.sh remove qwen3:1.7b"
        exit 1
    fi
    echo "🗑️  Removing model $1..."
    docker exec -it ollama ollama rm $1
}

# Function to show Ollama logs
show_logs() {
    echo "📜 Showing Ollama logs..."
    docker logs -f ollama
}

# Main script
case "$1" in
    "check")
        check_ollama
        ;;
    "wait")
        check_ollama
        wait_for_ollama
        ;;
    "list")
        check_ollama
        list_models
        ;;
    "pull")
        check_ollama
        pull_model "$2"
        ;;
    "run")
        check_ollama
        run_model "$2"
        ;;
    "remove")
        check_ollama
        remove_model "$2"
        ;;
    "logs")
        show_logs
        ;;
    *)
        echo "Usage: ./ollama-commands.sh <command> [model-name]"
        echo ""
        echo "Commands:"
        echo "  check     - Check if Ollama container is running"
        echo "  wait      - Wait for Ollama to be ready"
        echo "  list      - List all installed models"
        echo "  pull      - Pull a model (requires model name)"
        echo "  run       - Run a model interactively (requires model name)"
        echo "  remove    - Remove a model (requires model name)"
        echo "  logs      - Show Ollama logs"
        echo ""
        echo "Examples:"
        echo "  ./ollama-commands.sh pull qwen3:1.7b"
        echo "  ./ollama-commands.sh run qwen3:1.7b"
        echo "  ./ollama-commands.sh list"
        ;;
esac 