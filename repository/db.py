from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from odmantic import AIOEngine as __DATABASE_CLIENT
from starlette import status
from .config import DATABASE_URL as __DATABASE_URL
try:
     client = AsyncIOMotorClient(__DATABASE_URL)
     DATABASE = __DATABASE_CLIENT(client, database="computer_base_exam")
except Exception:
     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to database")

