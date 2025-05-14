#!/bin/sh

echo "Waiting for Ollama to be ready..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "Waiting for Ollama server..."
    sleep 2
done

echo "Ollama is ready! Starting automatic setup..."

# Pull default model
echo "Pulling default model (qwen3:1.7b)..."
ollama pull qwen3:1.7b

# You can add more commands here that you want to run automatically
# For example:
# echo "Pulling additional models..."
# ollama pull mistral
# ollama pull codellama

echo "Automatic setup completed!" 