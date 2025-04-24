FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y --no-install-recommends bash
COPY ./llama_run.sh .
ENV num_gpu=0


EXPOSE 11434
