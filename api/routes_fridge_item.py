from fastapi import APIRouter
from models.fridge_item import FridgeItemModel
from crud.fridge_item_crud import FridgeItemCRUD
from typing import List

from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog

log = TFLog.get_instance()
router = APIRouter(prefix="/fridge_item")

@router.get("/", response_model=List[FridgeItemModel])
async def get_items():
    return await FridgeItemCRUD.get_items()


@router.get("/{item_id}", response_model=FridgeItemModel)
async def get_item(item_id: str):
    return await FridgeItemCRUD.get_item(item_id)

@router.post("/", response_model=FridgeItemModel)
async def create_item(item: FridgeItemModel):
    item_id = item.id
    log.logger.info(f"try create fridge item id({item_id})")
    created = await FridgeItemCRUD.create_item(item)
    
    if not created:
        log.logger.warning(f"failed create fridge item id({item_id})")
        raise_bad_request()
    
    log.logger.info(f"success create fridge item id({item_id})")
    return created

@router.put("/", response_model=FridgeItemModel)
async def update_item(item: FridgeItemModel):
    item_id = item.id
    log.logger.info(f"try update fridge item id({item_id})")
    updated = await FridgeItemCRUD.update_item(item_id, item)
    
    if not updated:
        log.logger.warning(f"failed update fridge item id({item_id})")
        raise_bad_request()
    
    log.logger.info(f"success update fridge item id({item_id})")
    return updated

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    log.logger.info(f"try delete fridge item id({item_id})")
    await validate_item_id(item_id)
    deleted = await FridgeItemCRUD.delete_item(item_id)
    
    if not deleted:
        log.logger.warning(f"failed delete fridge item id({item_id})")
        raise_bad_request()
    
    log.logger.info(f"success delete fridge item id({item_id})")
    return {"message": f"Fridge item {item_id} deleted successfully"}


# util function
async def validate_item_id(item_id: str):
    """
    아이템 ID 존재 여부 체크
    """
    item = await FridgeItemCRUD.get_item(item_id)
    if not item:
        log.logger.warning(f"invalid fridge item id({item_id})")
        raise_not_found(detail="fridge item not found")
    return item