import requests
import logging
from typing import Union, BinaryIO
from typing import Dict
from config import (
    KEY,
    URL_EMBEDDINGS,
    URL_ALL_MODELS,
    URL_CHAT_COMPLETION,
    URL_COMPLETION_APPEALS,
    HEADERS_OPENAI,
    WHISPER_URL
)


def get_all_models() -> Dict:
    response = requests.get(URL_ALL_MODELS, headers={"Authorization": f"Bearer {KEY}"})
    logging.info(f"Request to get all models")

    if response.status_code == 200:
        logging.info(f"{response.status_code}")
        return response.json()
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.text)


def post_chat_completion(promt: str) -> Dict:
    response = requests.post(
        URL_CHAT_COMPLETION,
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "model": "llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": "Ты помощник"},
                {"role": "use", "content": promt},
            ],
            "temperature": 0.6,
            "max_tokens": 400,
            "n": 1,
            "presence_penalty": -0.6,
            "frequency_penalty": 1.0,
        },
    )
    logging.info(f"Request for post_chat_completion")
    if response.status_code == 200:
        logging.info(f"{response.status_code}")
        return response.json()
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.text)


def post_completion_appeals(promt: str) -> Dict:
    response = requests.post(
        URL_COMPLETION_APPEALS,
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "model": "llama-3.1-8b-instruct",
            "prompt": promt,
            "temperature": 0.6,
            "max_tokens": 200,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": [],
        },
    )
    logging.info(f"Request for post_completion_appeals")
    if response.status_code == 200:
        logging.info(f"{response.status_code}")
        return response.json()
    else:
        logging.error(f"Ошибка: {response.status_code}")
        logging.error(response.text)


def post_embeddings(promt: str) -> Dict:
    response = requests.post(
        URL_EMBEDDINGS,
        headers={"Authorization": f"Bearer {KEY}"},
        json={"model": "bge-m3", "input": promt},
    )
    logging.info(f"Request for post_embeddings")
    if response.status_code == 200:
        logging.info(f"{response.status_code}")
        return response.json()
    else:
        logging.error(f"Ошибка: {response.status_code}")
        logging.error(response.text)

def transcibe_audio(audio: Union[str, BinaryIO]):

    if isinstance(audio, str):
        audio = open(audio, "rb")

    req = requests.post(
        WHISPER_URL,
        headers=HEADERS_OPENAI,
        data=audio
    ).json()["text"]

    audio.close()
    return req
