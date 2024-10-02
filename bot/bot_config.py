from telegram import WebAppInfo
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: str = os.getenv('TOKEN')
'''
Можно юзать https://www.temporary-url.com/ для временных ссылок
'''
url_ru: str = ""  #An HTTPS URL
url_eng: str = ""  #An HTTPS URL

web_app_info_ru: WebAppInfo = WebAppInfo(url_ru)
web_app_info_eng: WebAppInfo = WebAppInfo(url_eng)
