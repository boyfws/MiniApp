import aiohttp
from .router import yandex_api_router


yandex_api_session = None

# Для примера логики работы
#@yandex_api_router.on_event("startup")
def get_yandex_api_session():
    global yandex_api_session
    yandex_api_session = aiohttp.ClientSession()

#@yandex_api_router.on_event("shutdown")
async def close_yandex_api_session() -> None:
    await yandex_api_session.close()


