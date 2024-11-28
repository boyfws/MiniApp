import aiohttp

yandex_api_session = aiohttp.ClientSession()


async def close_yandex_api_session() -> None:
    global yandex_api_session
    await yandex_api_session.close()

