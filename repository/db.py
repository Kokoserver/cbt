from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine as __DATABSE_CLIENT
from .config import DATABASE_URL as __DATABASE_URL

client = AsyncIOMotorClient(__DATABASE_URL)
db = __DATABSE_CLIENT(client, database="computer_base_exam")
