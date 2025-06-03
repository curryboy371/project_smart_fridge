import csv
import sys
from pathlib import Path
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manager.tfdb_manager import TFDB
from manager.tfconfig_manager import TFConfigManager as TFConfig
from core.tfenums import CollectionName

from pymongo.errors import BulkWriteError

from typing import Optional, List, Dict

# CSV 읽고 삽입
async def import_categorys():
    
    simple_collections = [
        CollectionName.NUTRITION,
        CollectionName.ALLERGIES,
        CollectionName.STORAGE_METHOD,
        CollectionName.FOOD_SIMPLE_CATEGORY,
    ]
    
    # 설정 로드 & DB 연결
    TFConfig.get_instance()
    db = TFDB.get_instance()
    if not await db.is_connected():
        print("[Error] MongoDB 연결 실패")
        return

    for col in simple_collections:
        collection = db.get_collection(col)
        csv_filename = f"{col.value}.csv"
        print(f'[Info] Read CSV {csv_filename}')

        filepath = os.path.join(os.path.dirname(__file__), 'csv', csv_filename)
        if not os.path.isfile(filepath):
            print(f"[Error] 파일이 존재하지 않습니다: {filepath}")
            continue

        # 기존 문서 삭제
        print("delete collection data")
        await collection.delete_many({})

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader]

            if not rows:
                print(f"[Warning] {csv_filename} 에 데이터가 없습니다.")
                continue

            await collection.insert_many(rows)
            print(f"[Info] {col.value} 컬렉션에 데이터 삽입 완료")

async def import_collection():
    # 설정 로드 & DB 연결
    TFConfig.get_instance()               # 설정을 사용할 곳이 따로 있으면 여기서 로드
    db = TFDB.get_instance()
    if not await db.is_connected():
        print("[Error] MongoDB 연결 실패")
        return

    collections = [
        CollectionName.USER_PROFILE,
        CollectionName.FOOD_CATEGORY,
        CollectionName.FRIDGE_ITEM,
        CollectionName.FRIDGE_LOG,      # log는 지워줌
    ]
    
    for col in collections:
        collection = db.get_collection(col)
        csv_filename = f"{col.value}.csv"
        print(f'[Info] Read CSV {csv_filename}')

        filepath = os.path.join(os.path.dirname(__file__), 'csv', csv_filename)
        if not os.path.isfile(filepath):
            print(f"[Error] 파일이 존재하지 않습니다: {filepath}")
            continue

        # 기존 문서 삭제
        await collection.delete_many({})
        print("delete collection data")

        # CSV 읽어 문서 삽입
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = [row for row in reader]

                # 컬렉션에 맞게 데이터 파싱    
                docs = []
                if col == CollectionName.USER_PROFILE:
                    docs = [preprocess_user_profile(row) for row in rows]
                elif col == CollectionName.FOOD_CATEGORY:
                    docs = [preprocess_food_category(row) for row in rows]
                elif col == CollectionName.FRIDGE_ITEM:
                    docs = [preprocess_fridge_item(row) for row in rows]
                    
                if not docs:
                    print("[Warn] CSV에 데이터가 없습니다.")
                    continue
                    
                result = await collection.insert_many(docs)
                print(f"[Success] {len(result.inserted_ids)}개 문서 삽입 완료")

        except FileNotFoundError:
            print(f"[Error] 파일이 존재하지 않습니다: {csv_filename}")
        except BulkWriteError as bwe:
            print(f"[Error] MongoDB 오류 {bwe.details}")
        except Exception as e:
            print(f"[Error] {e}")
            
        
def parse_list_field(value: str) -> List[str]:
    if not value or value.strip() == "":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def preprocess_user_profile(doc: dict) -> dict:
    """UserProfileModel에 맞게 CSV row(dict)를 전처리"""
    doc["age"] = int(doc["age"]) if doc.get("age") else None
    doc["allergies"] = parse_list_field(doc.get("allergies", ""))
    doc["preferredCategories"] = parse_list_field(doc.get("preferredCategories", ""))
    doc["notificationPreferences"] = parse_list_field(doc.get("notificationPreferences", ""))
    doc["missingNutrients"] = parse_list_field(doc.get("missingNutrients", ""))
    return doc     

def preprocess_food_category(doc: dict) -> dict:
    """FoodCategoryModel에 맞게 CSV row(dict)를 전처리"""
    doc["shelfLifeDays"] = int(doc["shelfLifeDays"]) if doc.get("shelfLifeDays") else 0
    doc["allergenTags"] = parse_list_field(doc.get("allergenTags", ""))
    doc["nutrition"] = parse_list_field(doc.get("nutrition", ""))
    return doc  

def preprocess_fridge_item(doc: dict) -> dict:
    return doc          
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python import_csv.py simple(default category) collection(collection data)")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "simple":
        print("import simple data")
        asyncio.run(import_categorys())
    elif mode == "collection":
        print("import collection data")
        asyncio.run(import_collection())
    else:
        print(f"알 수 없는 인자: {mode}")
        print("사용 가능한 인자: simple, collection")
        sys.exit(1)