from fastapi import APIRouter
from typing import List
from models.user_profile import UserProfileModel
from crud.generic_crud import GenericCRUD
from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog
from core import tfenums as en

class UserProfileAPI:
    def __init__(self, enum_value: en.CollectionName):
        self._enum_value = enum_value
        self._log = TFLog.get_instance()
        self._crud = GenericCRUD(enum_value)  # GenericCRUD로 변경

        # 라우터 등록
        self._router = APIRouter(prefix=f"/{self._enum_value.value}")

        # 라우터 핸들러 등록
        self._router.get("/", response_model=List[UserProfileModel])(self.get_profiles)
        self._router.get("/{user_id}", response_model=UserProfileModel)(self.get_profile)
        self._router.post("/", response_model=UserProfileModel)(self.create_profile)
        self._router.put("/", response_model=UserProfileModel)(self.update_profile)
        self._router.delete("/{user_id}")(self.delete_profile)

    @property
    def router(self):
        return self._router
    
    @property
    def crud(self):
        return self._crud

    async def get_profiles(self):
        return await self._crud.get_all()

    async def get_profile(self, user_id: str):
        profile = await self._crud.get_by_id(user_id)
        if not profile:
            self._log.logger.warning(f"invalid user id({user_id})")
            raise_not_found(detail="User not found")
        return profile

    async def create_profile(self, user_profile: UserProfileModel):
        user_id = user_profile.id
        self._log.logger.info(f"try create user id({user_id})")

        created = await self._crud.create(user_profile.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create user id({user_id})")
            raise_bad_request()

        self._log.logger.info(f"success create user id({user_id})")
        return created

    async def update_profile(self, user_profile: UserProfileModel):
        updated = await self._crud.update(user_profile.id, user_profile.dict(by_alias=True))
        if not updated:
            raise_bad_request()
        self._log.logger.info(f"success update user id({user_profile.id})")
        return updated
    
    async def delete_profile(self, user_id: str):
        self._log.logger.info(f"try delete user id({user_id})")

        deleted = await self._crud.delete(user_id)
        if not deleted:
            self._log.logger.warning(f"failed delete user id({user_id})")
            raise_bad_request()

        self._log.logger.info(f"success delete user id({user_id})")
        return {"message": f"User {user_id} deleted successfully"}