from bot.bot_api.bot_utils.storage import Storage
from bot.bot_api.config.bot_config import redis_url
import redis.asyncio as aioredis


redis_serv = aioredis.from_url(redis_url, decode_responses=False)
database = Storage(redis_serv)