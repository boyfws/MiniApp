from telegram import WebAppInfo
from dotenv import load_dotenv
from typing import cast
import os
from pathlib import Path

load_dotenv()

MAX_INLINE_BUTTON_LEN = 15

TOKEN: str = cast(str, os.getenv('BOT_TOKEN'))

url: str = "https://mini-app-test-prikol.duckdns.org/main"  #An HTTPS URL
web_app_info: WebAppInfo = WebAppInfo(url)


redis_host = os.getenv('REDIS_HOST')
redis_port = 6379
redis_password = os.getenv('REDIS_FOR_BOT_PASSWORD')
redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
