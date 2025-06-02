# api/chatgpt_router.py
from fastapi import APIRouter, HTTPException
from api.routes_exception import *
from api.routes_base import SimpleBaseAPI
from pydantic import BaseModel
from fastapi import Query
import os
import openai
from openai import AsyncOpenAI

from core.tflog import TFLoggerManager as TFLog

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatGPTAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("gpt")
        
        # 환경 변수에서 API 키 읽기
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")
        
        self.open_ai = AsyncOpenAI(api_key=api_key)

        self._router.post("/", response_model=ChatResponse)(self.chat_with_gpt)

    async def chat_with_gpt(self, request: ChatRequest):
        self._log.logger.info("chat chat gpt request")
        try:
            content = await ask_chatgpt(self.open_ai, request.message)
            self._log.logger.info("chat chat gpt request {content}")
            return {"response": content}
        except Exception as e:
            self._log.logger.error(f"GPT API Error: {e}")
            raise_bad_request(detail=str(e)) 


# GPT 서비스 함수
async def ask_chatgpt(client: AsyncOpenAI, message: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content