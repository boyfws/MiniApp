from telegram import WebAppInfo
from dotenv import load_dotenv
from typing import cast
import os

load_dotenv()

MAX_INLINE_BUTTON_LEN = 15

TOKEN: str = cast(str, os.getenv('TOKEN'))
'''
Можно юзать https://www.temporary-url.com/ для временных ссылок для теста
'''
url: str = "https://www.temporary-url.com/171"  #An HTTPS URL
web_app_info: WebAppInfo = WebAppInfo(url)


redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)

redis_url = f"redis://{redis_host}:{redis_port}"
if redis_password:
    redis_url += f"?password={redis_password}"