from enum import Enum

class CollectionName(Enum):
    USER_PROFILE = "user_profile"                   # 유저 정보 데이터
    FOOD_CATEGORY = "food_category"                 # 음식 정보 데이터 - 냉장고에서 보유한 것이 아닌 참고용
    FRIDGE_ITEM = "fridge_item"                     # 냉장고 음식 데이터
    FRIDGE_LOG = "fridge_log"                       # 음식 입출고 로그
    NUTRITION = "nutrition"                         # tpye-영양소 종류
    ALLERGIES = "allergies"                         # type-알러지 종류
    STORAGE_METHOD = "storage_method"               # type-보관 방법 종류
    FOOD_SIMPLE_CATEGORY = "food_simple_category"   # type-간단 음식 종류


# 냉장고 이벤트 ( 입고, 출고, 폐기 )
class EventType(Enum):
    INBOUND = "INBOUND"
    CONSUMED = "CONSUMED"
    DISCARDED = "DISCARDED"
    
    
class FridgePosition(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3