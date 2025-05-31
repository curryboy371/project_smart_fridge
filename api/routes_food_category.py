from fastapi import APIRouter
from models.food_category import FoodCategoryModel
from crud.food_category_crud import FoodCategoryCRUD
from typing import List

from api.routes_exception import *
from core.tflog import TFLoggerManager as TFLog

log = TFLog.get_instance()
router = APIRouter(prefix="/food_category")

@router.get("/", response_model=List[FoodCategoryModel])
async def get_categories():
    return await FoodCategoryCRUD.get_categories()

@router.get("/{category_id}", response_model=FoodCategoryModel)
async def get_category(category_id: str):
    return await validate_category_id(category_id)

@router.post("/", response_model=FoodCategoryModel)
async def create_category(category: FoodCategoryModel):
    category_id = category.id
    name = category.name
    log.logger.info(f"try create category id({category_id}), name({name})")

    # 중복 Name 검사
    exists_by_name = await FoodCategoryCRUD.get_category_by_name(name)
    if exists_by_name:
        log.logger.warning(f"duplicate name({name})")
        raise_conflict(detail="Category Name already exists")

    created = await FoodCategoryCRUD.create_category(category)
    if not created:
        log.logger.warning(f"failed create category id({category_id})")
        raise_bad_request()

    log.logger.info(f"success create category({category_id})")
    return created

@router.put("/", response_model=FoodCategoryModel)
async def update_category(category: FoodCategoryModel):
    category_id = category.id
    name = category.name
    log.logger.info(f"try update category id({category_id}), name({name})")

    updated = await FoodCategoryCRUD.update_category(category_id, category)
    if not updated:
        log.logger.warning(f"failed update category id({category_id})")
        raise_bad_request()

    log.logger.info(f"success update category({category_id})")
    return updated

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    log.logger.info(f"try delete category id({category_id})")

    deleted = await FoodCategoryCRUD.delete_category(category_id)
    if not deleted:
        log.logger.warning(f"failed delete category({category_id})")
        raise_bad_request()

    log.logger.info(f"success delete category({category_id})")
    return {"message": f"Category {category_id} deleted successfully"}


# 중복 검사용 함수
async def validate_category_id(category_id: str):
    category = await FoodCategoryCRUD.get_category(category_id)
    if not category:
        log.logger.warning(f"invalid category id({category_id})")
        raise_not_found(detail="Category not found")

    return category

