from fastapi import APIRouter
from api.routes_base import BaseAPI
from typing import List
from models.user_profile import UserProfileModel
import utils.exceptions
from core import tfenums as en

class UserProfileAPI(BaseAPI):
    def __init__(self, model, crud_class, enum_value):
        super().__init__(model, crud_class, enum_value)

        self._router.get("/{id}", response_model=self._model)(self.get_profile)
        self._router.post("/", response_model=self._model)(self.create_profile)
        self._router.put("/", response_model=self._model)(self.update_profile)
        self._router.delete("/{id}")(self.delete_profile)

    async def get_profiles(self):
        return await self._crud.get_all()
    
    async def get_profile(self, id: str):
        profile = await self._crud.get_by_id(id)
        if not profile:
            self._log.logger.warning(f"invalid user id({id})")
            utils.exceptions.raise_not_found(detail="User not found")
        return profile

    async def create_profile(self, user_profile: UserProfileModel):
        id = user_profile.id
        self._log.logger.info(f"try create user id({id})")

        created = await self._crud.create(user_profile.dict(by_alias=True))
        if not created:
            self._log.logger.warning(f"failed create user id({id})")
            utils.exceptions.raise_bad_request()

        self._log.logger.info(f"success create user id({id})")
        return created

    async def update_profile(self, user_profile: UserProfileModel):
        updated = await self._crud.update(user_profile.id, user_profile.dict(by_alias=True))
        if not updated:
            utils.exceptions.raise_bad_request()
        self._log.logger.info(f"success update user id({user_profile.id})")
        return updated
    
    async def delete_profile(self, id: str):
        self._log.logger.info(f"try delete user id({id})")

        deleted = await self._crud.delete(id)
        if not deleted:
            self._log.logger.warning(f"failed delete user id({id})")
            utils.exceptions.raise_bad_request()

        self._log.logger.info(f"success delete user id({id})")
        return {"message": f"User {id} deleted successfully"}