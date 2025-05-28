from fastapi import APIRouter
from models.food_category import FoodCategoryModel
from crud.food_category_crud import FoodCategoryCRUD
from typing import List


router = APIRouter(prefix="/food_category")

@router.get("/", response_model=List[FoodCategoryModel])
async def get_categories():
    return await FoodCategoryCRUD.get_categories()

@router.get("/{category_id}", response_model=FoodCategoryModel)
async def get_category(category_id: str):
    return await FoodCategoryCRUD.get_category(category_id)

@router.post("/", response_model=FoodCategoryModel)
async def create_category(category: FoodCategoryModel):
    return await FoodCategoryCRUD.create_category(category)

@router.delete("/{user_id}")
async def delete_category(category: FoodCategoryModel):
    return await FoodCategoryCRUD.delete_category(category)