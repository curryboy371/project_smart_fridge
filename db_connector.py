from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "mydatabase"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.user_collection = self.db.users

    async def is_connected(self):
        try:
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            print("MongoDB 연결 실패:", e)
            return False

db = Database()