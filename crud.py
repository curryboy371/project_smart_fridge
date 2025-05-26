from typing import List, Optional
from bson import ObjectId
from models import UserModel
from db_connector import db

class UserCRUD:
    collection = db.user_collection
    
    @classmethod
    async def create_user(cls, user: UserModel) -> dict:
        user_dict = user.dict(by_alias=True)
        user_dict.pop("_id", None)  # _id 제거
        result = await cls.collection.insert_one(user_dict)
        created_user = await cls.collection.find_one({"_id": result.inserted_id})
        return created_user

    @classmethod
    async def get_users(cls) -> List[dict]:
        users = []
        cursor = cls.collection.find()
        async for user in cursor:
            users.append(user)
        return users

    @classmethod
    async def get_user(cls, user_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        return user

    @classmethod
    async def update_user(cls, user_id: str, user: UserModel) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        user_dict = user.dict(by_alias=True)
        user_dict.pop("_id", None)
        result = await cls.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
        if result.matched_count == 0:
            return None
        updated_user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        return updated_user

    @classmethod
    async def delete_user(cls, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await cls.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0