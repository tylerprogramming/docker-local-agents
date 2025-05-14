#!/bin/sh

# echo "Starting Ollama server..."
# ollama serve &
# OLLAMA_PID=$!

# # Wait for Ollama to be ready
# echo "Waiting for Ollama server to be ready..."
# while ! curl -s http://localhost:11434/api/tags > /dev/null; do
#     echo "Waiting for Ollama server..."
#     sleep 2
# done

# echo "Ollama server is ready!"

# # Pull the model
# echo "Pulling qwen3:1.7b model..."
# ollama pull qwen3:1.7b

# echo "Model pull completed!"

# # Keep the container running
# wait $OLLAMA_PID
