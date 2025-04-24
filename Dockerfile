FROM python:3.11-slim
ENV PYTHONPATH="${PYTHONPATH}:/app"
WORKDIR /app

COPY . .
COPY interface .

RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends bash

EXPOSE 8000 8501
