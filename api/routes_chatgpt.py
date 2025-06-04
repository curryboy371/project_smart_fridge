# api/chatgpt_router.py
from fastapi import APIRouter, HTTPException
import utils.exceptions
from api.routes_base import SimpleBaseAPI
from pydantic import BaseModel
from fastapi import Query
import os
import openai
from openai import AsyncOpenAI
import json
from typing import List, Type
import core.tfenums as en
from manager.crud_manager import CrudManager


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

        self._router.get("/test", response_model=ChatResponse)(self.chat_with_gpt_test)
        self._router.get("/", response_model=ChatResponse)(self.chat_with_gpt)

    async def chat_with_gpt(self):
        self._log.logger.info("chat chat gpt request")

        # 인원  정보    ...
        user_profile_crud = CrudManager.get_instance().get_crud(en.CollectionName.USER_PROFILE)
        users = await user_profile_crud.get_all()
        user_results = []
        for user in users:
            username = user["username"]
            age = user["age"]
            gender = user["gender"]
            allergies = user["allergies"]
            preferredCategories = user["preferredCategories"]
            missingNutrients = user["missingNutrients"]
            
            user_results.append({
                "username": username,
                "age": age,
                "gender": gender,
                "allergies": allergies,
                "preferredCategories": preferredCategories,
                "missingNutrients": missingNutrients,
            })
            
        # 유통기한 안 넘은 음식만...
        fridge_item_crud = CrudManager.get_instance().get_crud(en.CollectionName.FRIDGE_ITEM)
        food_category_crud = CrudManager.get_instance().get_crud(en.CollectionName.FOOD_CATEGORY)
        not_expired_items = await fridge_item_crud.get_not_expired_items()
        
        food_results = []
        for item in not_expired_items:
            name = item.get("name")
            category_name = item.get("food_category")
            allergies = []
            nutritions = []
            
            if category_name:
                print("find food category")
                category = await food_category_crud.get_by_name(name)
                if not category:
                    category = await food_category_crud.get_by_food_category_name(category_name)

                if category:
                    allergies = category.get("allergenTags", [])
                    nutritions = category.get("nutrition", [])

            food_results.append({
                "food name": name,
                "allergies": allergies,
                "nutrition": nutritions
            })
        
        if not user_results:
            return {"response": "유저 정보가 없습니다."}    
            
        if not food_results:
            return {"response": "유통기한이 지나지 않은 음식이 없습니다."}    
            
        try:
            user_json = json.dumps(user_results, ensure_ascii=False, indent=2)
            food_json = json.dumps(food_results, ensure_ascii=False, indent=2)
            
            # GPT에게 보낼 프롬프트 구성
            prompt = (
                f"다음은 사용자 프로필 리스트입니다:\n{user_json}\n\n"
                f"다음은 유통기한이 지나지 않은 음식 리스트입니다:\n{food_json}\n\n"
                "각 사용자에게 적절한 음식을 추천해주세요.\n"
                "추천 이유도 간단하게 설명해 주세요.\n"
                "각 사용자의 알러지와 부족한 영양소를 고려해서 추천해야 합니다."
            )
            content = await ask_chatgpt(self.open_ai, prompt)
            self._log.logger.info("chat chat gpt request {content}")
            return {f"response": content}
        
        except Exception as e:
            self._log.logger.error(f"GPT API Error: {e}")
            utils.exceptions.raise_bad_request(detail=str(e)) 

    async def chat_with_gpt_test(self):
        self._log.logger.info("chat chat gpt request test")
        return {"response": "gpt text test gpt text testgpt text testgpt text testgpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text testgpt text test"
        "gpt text testgpt text testgpt text testgpt text testgpt text test"
        }
    


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