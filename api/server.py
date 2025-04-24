from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging
from typing import Optional
from config import (
    KEY,
    URL_EMBEDDINGS,
    URL_ALL_MODELS,
    URL_CHAT_COMPLETION,
    URL_COMPLETION_APPEALS,
)

app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = "llama-3.1-8b-instruct"
    temperature: Optional[float] = 0.6
    max_tokens: Optional[int] = 200


class CompletionRequest(BaseModel):
    prompt: str
    model: Optional[str] = "llama-3.1-8b-instruct"
    temperature: Optional[float] = 0.6
    max_tokens: Optional[int] = 200


class EmbeddingsRequest(BaseModel):
    prompt: str
    model: Optional[str] = "bge-m3"


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.get("/api/v1/get_models")
async def get_models():
    try:
        response = requests.get(
            URL_ALL_MODELS, headers={"Authorization": f"Bearer {KEY}"}
        )
        logger.info(f"Request to get all models")

        if response.status_code == 200:
            logger.info(f"Success: {response.status_code}")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chat_completion")
async def chat_completion(request: ChatRequest):
    try:
        payload = {
            "model": request.model,
            "messages": [
                {"role": "system", "content": "Ты помощник"},
                {"role": "user", "content": request.prompt},
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "n": 1,
            "presence_penalty": -0.6,
            "frequency_penalty": 1.0,
        }

        response = requests.post(
            URL_CHAT_COMPLETION,
            headers={"Authorization": f"Bearer {KEY}"},
            json=payload,
        )
        logger.info(
            f"Request for chat completion with prompt: {request.prompt[:50]}..."
        )

        if response.status_code == 200:
            logger.info(f"Success: {response.status_code}")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/completion_appeals")
async def completion_appeals(request: CompletionRequest):
    try:
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": [],
        }

        response = requests.post(
            URL_COMPLETION_APPEALS,
            headers={"Authorization": f"Bearer {KEY}"},
            json=payload,
        )
        logger.info(
            f"Request for completion appeals with prompt: {request.prompt[:50]}..."
        )

        if response.status_code == 200:
            logger.info(f"Success: {response.status_code}")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/embeddings")
async def get_embeddings(request: EmbeddingsRequest):
    try:
        payload = {"model": request.model, "input": request.prompt}

        response = requests.post(
            URL_EMBEDDINGS, headers={"Authorization": f"Bearer {KEY}"}, json=payload
        )
        logger.info(f"Request for embeddings with prompt: {request.prompt[:50]}...")

        if response.status_code == 200:
            logger.info(f"Success: {response.status_code}")
            return response.json()
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
