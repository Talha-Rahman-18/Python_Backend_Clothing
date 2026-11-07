import logging

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

client = AsyncMongoClient(
    settings.MONGODB_URI,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=50,
)

db: AsyncDatabase = client[settings.DATABASE_NAME]


async def connect_to_mongodb() -> None:
    await client.admin.command("ping")
    logger.info("MongoDB connection established!!")


async def close_mongodb_connection() -> None:
    await client.close()
    logger.info("MongoDB connection closed")