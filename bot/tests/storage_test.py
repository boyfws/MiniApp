from redis import asyncio as aioredis
import os
import pytest
import pytest_asyncio
from bot.bot_api.bot_utils.storage import Storage
import asyncio
import time

### Моки добавлю позже!!!!!

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)
# Формирование URL для подключения
redis_url = f"redis://{redis_host}:{redis_port}"
if redis_password:
    redis_url += f"?password={redis_password}"
redis = aioredis.from_url(redis_url, decode_responses=False)


@pytest.fixture(scope="session")
def event_loop():
    global redis
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        # Выполнить асинхронные команды перед закрытием цикла
        loop.run_until_complete(cleanup_redis(loop))
        loop.close()


async def cleanup_redis(loop) -> None:
    global redis
    if redis:
        await redis.flushall()  # Чистим всю бд
        await redis.close()


def test_wrong_database() -> None:
    with pytest.raises(ValueError) as e:
        Storage(10)


def test_normal_database() -> None:
    Storage(redis)


@pytest.mark.parametrize("key",
                         (
                                 (b"Aboba",),
                                 (213,),
                                 (complex(2, 2))
                         )
                         )
@pytest.mark.asyncio
async def test_non_str_key(key) -> None:
    db = Storage(redis)
    with pytest.raises(ValueError) as e:
        await db.add_dict(key, 20)
    assert str(e.value) == f"Аргумент {'key'} имеет неверный тип данных, ожидался {str}, получен {type(key)}"

### Валидацию аргументов более не трогаем там на все одна функция


@pytest.mark.asyncio
async def test_non_int_lifetime() -> None:
    db = Storage(redis)
    lifetime = 100.1
    with pytest.raises(ValueError) as e:
        await db.add_dict("dada", lifetime)
    assert str(e.value) == f"Аргумент {'lifetime'} имеет неверный тип данных, ожидался {int}, получен {type(lifetime)}"


@pytest.mark.asyncio
async def test_same_dict_creation() -> None:
    db = Storage(redis)
    await db.add_dict("Papa", 10)
    with pytest.raises(ValueError) as e:
        await db.add_dict("Papa", 10)
    assert str(e.value) == f"Ключ Papa уже существует в базе данных"


@pytest.mark.asyncio
async def test_del_dict() -> None:
    db = Storage(redis)
    await db.add_dict("Mama", 10)
    count = await db.del_dict("Mama")
    await db.add_dict("Mama", 10)
    assert count == 1


@pytest.mark.asyncio
async def test_to_add_value_without_init() -> None:
    with pytest.raises(ValueError) as e:
        await Storage(redis).add_values_to_dict("papa", {"dada": 1})

    assert str(e.value) == "Указанный ключ не найден в базе данных"


@pytest.mark.asynco
async def test_all_available_data_types() -> None:
    data = {"int": 1,
            "float": 1.21,
            "str": "abaoba",
            "binary_string": b'dadada',
            "list": [1, 2],
            "bool": True,
            "none": None}
    db = Storage(redis)
    await db.add_dict("Ratata", 10 ** 5)
    await db.add_values_to_dict("Ratata", data)
    same_dict = await db.get_dict("Ratata")
    assert same_dict == data


@pytest.mark.parametrize("data", (
        (complex(2, 2),),
        ({2, 2, 3},),
        ((1, 2, 3),),
        ({1: "dsa", "dad": 3})
))
@pytest.mark.asynco
async def test_wrong_data_type(data) -> None:
    db = Storage(redis)
    await db.add_dict("dada_aaa", 1000)
    with pytest.raises(ValueError) as e:
        await db.add_values_to_dict("dada_aaa", {"key": data})
    await db.del_dict("dada_aaa")
    assert str(e.value) == f"Введен неподходящий тип данных: {type(data)}"


@pytest.mark.asynco
async def test_ndarray() -> None:
    db = Storage(redis)
    data = [[212, 121], "esda"]
    await db.add_dict("dada_aaa", 1000)
    with pytest.raises(ValueError) as e:
        await db.add_values_to_dict("dada_aaa", {"key": data})
    await db.del_dict("dada_aaa")
    assert str(e.value) == f"Передан вложенный список {data}"


@pytest.mark.asynco
async def test_lifetime_arg() -> None:
    db = Storage(redis)
    key = "adadadada"
    data = {"lifetime": "dada"}
    await db.add_dict(key, 5)
    with pytest.raises(ValueError) as e:
        await db.add_values_to_dict(key, data)
    assert str(e.value) == f"Ключ для словаря не может быть равен lifetime"


@pytest.mark.asynco
async def test_autodelete() -> None:
    db = Storage(redis)
    key = "dada_aaa"
    data = {"dada": "dada"}
    await db.add_dict(key, 5)
    await db.add_values_to_dict(key, data) # Выполняем операцию, чтобы начать отсчет
    time.sleep(5 * 1.05) # + 5 % на погрешность
    with pytest.raises(ValueError) as e:
        await db.get_dict(key)
    assert str(e.value) == f"Ключ {key} не существует в базе данных"


@pytest.mark.asynco
async def test_refresh_time_for_autodelete() -> None:
    db = Storage(redis)
    key = "key_one_more"
    data1 = {"dada": "dada"}
    data2 = {"ratata": "dadqe"}
    await db.add_dict(key, 5)
    await db.add_values_to_dict(key, data1)  # Выполняем операцию, чтобы начать отсчет
    time.sleep(2)
    await db.add_values_to_dict(key, data1)  # Счетчик должен обновиться
    time.sleep(3)
    await db.get_dict(key) # Если есть ошибка в обновлении счетчика запись удалится
    time.sleep(5 * 1.05) # Получение словаря обновляет счетчик
    with pytest.raises(ValueError) as e:
        await db.get_dict(key) # Запись уже должна удалиться
    assert str(e.value) == f"Ключ {key} не существует в базе данных"


@pytest.mark.asynco
async def test_delete_inside_dict() -> None:
    data = {"int": 1,
            "float": 1.21,
            "str": "abaoba",
            "binary_string": b'dadada',
            "list": [1, 2],
            "bool": True,
            "none": None}
    to_del = ["none", "bool"]
    key = "aboba228"
    db = Storage(redis)
    await db.add_dict(key, 10 ** 5)
    await db.add_values_to_dict(key, data)
    await db.del_values_from_dict(key, to_del)
    for  el in to_del:
        del data[el]

    same_dict = await db.get_dict(key)
    assert same_dict == data


@pytest.mark.asynco
async def test_get_values_from_empty_dict() -> None:
    db = Storage(redis)
    with pytest.raises(ValueError) as e:
        await db.get_values_from_dict("dadadada", ["1", "2", "3"])
    assert str(e.value) == "Указанный ключ не найден в базе данных"


@pytest.mark.asynco
async def test_get_values_from_empty_keys() -> None:
    data = {"int": 1,
            "float": 1.21,
            "str": "abaoba",
            "binary_string": b'dadada',
            "list": [1, 2],
            "bool": True}
    to_get = ["none", "bool", "banana", "sobAKA"]
    key = "aboba228num2"
    db = Storage(redis)
    await db.add_dict(key, 10 ** 5)
    await db.add_values_to_dict(key, data)
    one_more_dict = await db.get_values_from_dict(key, to_get)
    print(one_more_dict)
    assert one_more_dict == {key: data[key] for key in data if key in to_get}





















