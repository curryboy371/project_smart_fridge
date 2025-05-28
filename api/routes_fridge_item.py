from fastapi import APIRouter
from models.fridge_item import FridgeItemModel
from crud.fridge_item_crud import FridgeItemCRUD
from typing import List


router = APIRouter(prefix="/fridge_item")

@router.get("/", response_model=List[FridgeItemModel])
async def get_items():
    return await FridgeItemCRUD.get_items()

@router.get("/{item_id}", response_model=FridgeItemModel)
async def get_item(item_id: str):
    return await FridgeItemCRUD.get_item(item_id)

@router.post("/", response_model=FridgeItemModel)
async def create_item(item: FridgeItemModel):
    return await FridgeItemCRUD.create_item(item)

@router.delete("/{item_id}")
async def delete_item(item: FridgeItemModel):
    return await FridgeItemCRUD.delete_item(item)