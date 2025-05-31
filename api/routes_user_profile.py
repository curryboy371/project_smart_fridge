from fastapi import APIRouter
from models.user_profile import UserProfileModel
from crud.user_profile_crud import UserProfileCRUD
from typing import List

from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog

log = TFLog.get_instance()
router = APIRouter(prefix="/user_profile")

# get 조회
@router.get("/", response_model=List[UserProfileModel])
async def get_user_profiles():
    return await UserProfileCRUD.get_user_profiles()

@router.get("/{user_id}", response_model=UserProfileModel)
async def get_user_profile(user_id: str):
    return await UserProfileCRUD.get_user_profile(user_id)

# put 수정
@router.put("/", response_model=UserProfileModel)
async def update_user_profile(user_profile: UserProfileModel):
    user_id = user_profile.id
    log.logger.info(f"try put user id({user_id})")
    await validate_user_id(user_id)
    updated_user = await UserProfileCRUD.update_user_profile(user_id, user_profile)
    
    if not updated_user:
        log.logger.warning(f"failed update id({user_id})")
        raise_bad_request()
    
    log.logger.info(f"success patch user({user_id})")
    return updated_user

# post 입력
@router.post("/", response_model=UserProfileModel)
async def create_user_profile(user_profile: UserProfileModel):
    user_id = user_profile.id
    log.logger.info(f"try create user id({user_id})")
    created = await UserProfileCRUD.create_user_profile(user_profile)
    
    if not created:
        log.logger.warning(f"failed create id({user_id})")
        raise_bad_request()
        
    log.logger.info(f"succss create user({user_id})")
    return created

# delete 제거
@router.delete("/{user_id}")
async def delete_user_profile(user_id: str):
    log.logger.info(f"try delete user id({user_id})")
    await validate_user_id(user_id)
    deleted = await UserProfileCRUD.delete_user_profile(user_id)
    if not deleted:
        log.logger.warning(f"failed delete id({user_id})")
        raise_bad_request()
        
    log.logger.info(f"succss delete user({user_id})")
    return {"message": f"User {user_id} deleted successfully"}
        

# util fucntion
async def validate_user_id(user_id):
    """
    기존 유저가 있는지 체크
    """
    user = await UserProfileCRUD.get_user_profile(user_id)
    if not user:
        log.logger.warning(f"invalid user id({user_id})")
        raise_not_found(detail="user not found")
    return user