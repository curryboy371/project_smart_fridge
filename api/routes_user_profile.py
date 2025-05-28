from fastapi import APIRouter
from models.user_profile import UserProfileModel
from crud.user_profile_crud import UserProfileCRUD
from typing import List


router = APIRouter(prefix="/user_profile")

@router.get("/", response_model=List[UserProfileModel])
async def get_user_profiles():
    return await UserProfileCRUD.get_user_profiles()

@router.get("/{user_id}", response_model=UserProfileModel)
async def get_user_profile(user_id: str):
    return await UserProfileCRUD.get_user_profile(user_id)

@router.post("/", response_model=UserProfileModel)
async def create_user_profile(user_profile: UserProfileModel):
    return await UserProfileCRUD.create_user_profile(user_profile)

@router.delete("/{user_id}")
async def delete_user_profile(user_profile: UserProfileModel):
    return await UserProfileCRUD.delete_user_profile(user_profile)