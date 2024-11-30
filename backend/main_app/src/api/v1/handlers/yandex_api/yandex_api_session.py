import aiohttp
from dataclasses import dataclass


@dataclass
class YandexApiSession:
    session: aiohttp.ClientSession | None = None


yandex_api_session = YandexApiSession()


async def open_yandex_api_session():
    global yandex_api_session
    yandex_api_session.session = aiohttp.ClientSession()


async def close_yandex_api_session() -> None:
    global yandex_api_session
    await yandex_api_session.session.close()

