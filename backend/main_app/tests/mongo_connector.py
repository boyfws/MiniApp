from contextlib import asynccontextmanager
from src.database.mongo_db import AsyncMongoDB
from src.config import configuration
@asynccontextmanager
async def get_test_db() -> AsyncMongoDB:
    yield AsyncMongoDB(collection_name=configuration.mongo_db.test_menu_collection)