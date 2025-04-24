#!/bin/bash

nuhup ollama serve &

for i in $(seq 1 1000); do \
        sleep 2; \
        if curl -s http://localhost:11434/health; then \
            echo "Ollama server is up!"; \
            break; \
        fi; \
        echo "Waiting for Ollama server..."; \
    done

ollama pull llama3
ollama pull mistral
ollama pull llama2
