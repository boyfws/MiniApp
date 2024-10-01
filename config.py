from telegram import WebAppInfo

TOKEN: str = ""
'''
Можно юзать https://www.temporary-url.com/ для временных ссылок
'''
url_ru: str = ""  #An HTTPS URL
url_eng: str = ""  #An HTTPS URL

web_app_info_ru: WebAppInfo = WebAppInfo(url_ru)
web_app_info_eng: WebAppInfo = WebAppInfo(url_eng)
