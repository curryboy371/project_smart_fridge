from typing import List, Optional
from bson import ObjectId
from models.user_profile import UserProfileModel
from core.tfdb import TFDB


class UserProfileCRUD:

    collection = TFDB.get_instance().user_profile_collection  # ⚠️ 컬렉션 이름 확인 필요

    @classmethod
    async def create_user_profile(cls, user_profile: UserProfileModel) -> dict:
        user_dict = user_profile.dict(by_alias=True)
        user_dict.pop("_id", None)  # _id 제거 (MongoDB가 자동 생성)
        result = await cls.collection.insert_one(user_dict)
        created_user = await cls.collection.find_one({"_id": result.inserted_id})
        return created_user

    @classmethod
    async def get_user_profiles(cls) -> List[dict]:
        users = []
        cursor = cls.collection.find()
        async for user in cursor:
            users.append(user)
        return users

    @classmethod
    async def get_user_profile(cls, user_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        return user

    @classmethod
    async def update_user_profile(cls, user_id: str, user_profile: UserProfileModel) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        user_dict = user_profile.dict(by_alias=True)
        user_dict.pop("_id", None)
        result = await cls.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
        if result.matched_count == 0:
            return None
        updated_user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        return updated_user

    @classmethod
    async def delete_user_profile(cls, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await cls.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0