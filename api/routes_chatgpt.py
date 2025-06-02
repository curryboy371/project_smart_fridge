# api/chatgpt_router.py
from fastapi import APIRouter, HTTPException
from api.routes_exception import *
from api.routes_base import SimpleBaseAPI
from pydantic import BaseModel
import openai
from fastapi import Query

from core.tflog import TFLoggerManager as TFLog

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatGPTAPI(SimpleBaseAPI):
    def __init__(self):
        super().__init__("gpt")

        self._router.post("/", response_model=ChatResponse)(self.chat_with_gpt)
        self._router.get("/", response_model=ChatResponse)(self.test_chat_with_gpt)

    @property
    def router(self):
        return self._router
    
    @property
    def tag(self):
        return self._tag
    
    async def test_chat_with_gpt(self):
        self._log.logger.info("test chat gpt!!")
        return {"response": f"test!!! GPT"}

    async def chat_with_gpt(self, request: ChatRequest):
        self._log.logger.info("chat chat gpt request")
        try:
            content = await ask_chatgpt(request.message)
            self._log.logger.info("chat chat gpt request {content}")
            return {"response": content}
        except Exception as e:
            raise_bad_request(detail=e)


# gpt services
async def ask_chatgpt(message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message["content"]