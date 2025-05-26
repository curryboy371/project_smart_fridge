from fastapi import FastAPI, HTTPException
from typing import List
from models import UserModel
from db_connector import db
from crud import UserCRUD

app = FastAPI()
UserCRUD.collection.insert_many

@app.on_event("startup")
async def startup_event():
    connected = await db.is_connected()
    if not connected:
        # 로그 남기거나 예외 발생 가능
        print("MongoDB 연결 실패! 서버 종료를 고려하세요.")
        
        
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI + MongoDB!"}

@app.post("/users/", response_model=UserModel)
async def create_user(user: UserModel):
    user_dict = user.dict(by_alias=True)
    result = await db.user_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)  # ObjectId -> str 변환
    return user_dict

@app.get("/users/", response_model=List[UserModel])
async def get_users():
    users = await UserCRUD.get_users()
    return users

@app.get("/users/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user = await UserCRUD.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found or invalid ID")
    return user

@app.put("/users/{user_id}", response_model=UserModel)
async def update_user(user_id: str, user: UserModel):
    updated = await UserCRUD.update_user(user_id, user)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found or invalid ID")
    return updated

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    success = await UserCRUD.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or invalid ID")
    return {"message": "User deleted successfully"}