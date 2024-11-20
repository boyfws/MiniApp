from telegram import WebAppInfo
from dotenv import load_dotenv
from typing import cast
import os
from pathlib import Path

load_dotenv(dotenv_path=Path.cwd().parent / ".env")

MAX_INLINE_BUTTON_LEN = 15

TOKEN: str = cast(str, os.getenv('TOKEN'))
'''
Можно юзать https://www.temporary-url.com/ для временных ссылок для теста
'''
url: str = "https://www.temporary-url.com/171"  #An HTTPS URL
web_app_info: WebAppInfo = WebAppInfo(url)


redis_host = os.getenv('REDIS_HOST')
redis_port = 6379
redis_password = os.getenv('REDIS_FOR_BOT_PASSWORD')
redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
