from telegram import WebAppInfo
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: str = os.getenv('TOKEN')
'''
Можно юзать https://www.temporary-url.com/ для временных ссылок для теста
'''
url: str = ""  #An HTTPS URL
web_app_info: WebAppInfo = WebAppInfo(url)
