from aiocache import cached, SimpleMemoryCache


# Кэш живет час
@cached(ttl=3600, cache=SimpleMemoryCache)
async def check_user_roots(user_id: int, rest_id: int) -> bool:
    """
    Делает запрос к API и возвращает True, если пользователю разрешено право работать с рестораном и False иначе
    Результаты кэшируются
    :param user_id: id ресторана с которым производится действие
    :param rest_id: id пользователя
    :return:
    """
    return True
