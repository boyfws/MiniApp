from .storage import Storage
from bot_api.config import redis_url
import redis.asyncio as aioredis


redis_serv = aioredis.from_url(redis_url, decode_responses=False)
database = Storage(redis_serv)