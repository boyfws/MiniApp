from types import NoneType
from redis import asyncio as aioredis
from typing import Dict, Optional, Any, Set, List
import json
import base64


class Storage:
    """
    Класс реализует взаимодействие с redis с сохранением типов данных

    Используется для хранения словарей в redis

    Поддерживаемые типы данных:
    1) Числовые: float, int
    2) str, binary string
    3) bool
    4) None
    5) Одномерный list

    Каждый ключ имеет время жизни, если с ним не происходило действий в течение этого времени
    он удаляется

    Реализована строгая проверка на типы данных
    """
    _available_dtypes: Set[type] = {float, int, NoneType, str, bool, list, bytes}

    def __init__(self, database: aioredis.Redis) -> None:
        self._validate_arg(arg_name="database", expected=aioredis.Redis, data=database)

        self._db: aioredis.Redis = database  # decode-responses: False!!!!

    @staticmethod
    def _validate_arg(arg_name: str, expected: type, data: Any) -> None:
        """
        Валидирует тип данных аргумента
        :param arg_name: Имя аргумента для информационного сообщения
        :param expected: Ожидаемый тип данных аргумента
        :param data: Данные для проверки
        :return:

        """
        if not isinstance(data, expected):
            raise ValueError(
                f"Аргумент {arg_name} имеет неверный тип данных, ожидался {expected}, получен {type(data)}")

    def _pack_data(self, data: Any) -> str:
        """
        Подготавливает данные к оправке в redis
        :param data: Входные данные тип данных из _available_dtypes
        :return: Данные в формате str
        """
        if type(data) not in self._available_dtypes:
            raise ValueError(f"Введен неподходящий тип данных: {type(data)}")

        if isinstance(data, bytes):
            packed_data = base64.b64encode(data).decode('utf-8')
            return json.dumps(
                {
                    "binary": True,
                    "data": packed_data
                }
            )

        elif isinstance(data, list):
            for el in data:
                if type(el) not in self._available_dtypes:
                    raise ValueError(f"Введен неподходящий тип данных: {type(el)}")

                if isinstance(el, list):
                    raise ValueError(f"Передан вложенный список {data}")

        return json.dumps(
            {
                "binary": False,
                "data": data
            }
        )

    def _unpack_data(self, data: bytes) -> Any:
        """
        Распаковывает данные из redis в формате бинарных строк
        :param data:
        :return: Данные в исходном формате
        """
        unpacked_data = json.loads(data)
        if unpacked_data["binary"]:
            return base64.b64decode(unpacked_data["data"].encode('utf-8'))

        return unpacked_data["data"]

    async def add_dict(self, key: str, lifetime: Optional[int] = 10) -> None:
        """
        Добавляет словарь в базу данных
        :param key: Новый словарь в базе данных
        :param lifetime: Время жизни в секундах
        :return:
        """
        self._validate_arg(arg_name="key", expected=str, data=key)
        self._validate_arg(arg_name="lifetime", expected=int, data=lifetime)

        if await self._db.exists(key):
            raise ValueError(f"Ключ {key} уже существует в базе данных")

        await self._db.hset(key, "lifetime", self._pack_data(lifetime))

    async def del_dict(self, key: str) -> int:
        """
        Команда для удаления словаря
        :param key:
        :return: 1 если ключ удален, 0 в прочих случаях
        """
        self._validate_arg(arg_name="key", expected=str, data=key)
        return await self._db.delete(key)

    async def get_dict(self, key: str) -> Dict[str, Any]:
        """
        Возвращает весь словарь по ключу
        :param key: Ключ для словаря
        :return:
        """
        self._validate_arg(arg_name="key", expected=str, data=key)

        await self._db.expire(key, 100)  # Нужно чтобы ключ не удалился во время выполнения
        response_dict = await self._db.hgetall(key)

        if response_dict == {}:
            raise ValueError(f"Ключ {key} не существует в базе данных")

        return_dict = {
            key.decode('utf-8'): self._unpack_data(response_dict[key]) for key in response_dict
        }

        await self._db.expire(key, return_dict["lifetime"])
        del return_dict["lifetime"]
        return return_dict

    async def del_values_from_dict(self, key: str, data_to_del: List[str]) -> int:
        """
        Удаляет ключи в словаре доступном по key
        :param key:
        :param data_to_del:
        :return: Количество удаленных полей
        """
        for el in data_to_del:
            self._validate_arg(arg_name="data_to_del_el", expected=str, data=el)

        return await self._db.hdel(key, *data_to_del)

    async def add_values_to_dict(self, key: str, data_to_add: Dict[str, Any]) -> None:
        """
        Добавляет значения в словарь доступный по ключу key
        :param key: Ключ для словаря
        :param data_to_add: Данные в формате {ключ: значение}
        :return:
        """
        self._validate_arg(arg_name="key", expected=str, data=key)
        self._validate_arg(arg_name="data_to_add", expected=dict, data=data_to_add)

        if not await self._db.exists(key):
            raise ValueError("Указанный ключ не найден в базе данных")

        await self._db.expire(key, 100)  # Устанавливаем время жизни с запасом для выполнения операций
        mapping_dict = {}

        for el in data_to_add:
            self._validate_arg(arg_name="data_to_add[key]", expected=str, data=el)

            if el == "lifetime":
                raise ValueError("Ключ для словаря не может быть равен lifetime")

            mapping_dict[el] = self._pack_data(data_to_add[el])

        await self._db.hset(key, mapping=mapping_dict)
        time_to_live = self._unpack_data(await self._db.hget(key, "lifetime"))
        await self._db.expire(key, time_to_live)

    async def get_values_from_dict(self, key: str, data_to_get: List[str]) -> Dict[str, Any]:
        """
        Получает значения из словаря доступного по key
        Значения передаются в массиве data_to_get, если значения нет в словаре оно игнорируется
        :param key:
        :param data_to_get:
        :return:
        """
        self._validate_arg(arg_name="key", expected=str, data=key)
        self._validate_arg(arg_name="data_to_add", expected=list, data=data_to_get)

        if not await self._db.exists(key):
            raise ValueError("Указанный ключ не найден в базе данных")

        await self._db.expire(key, 100)  # Устанавливаем время жизни с запасом для выполнения операций

        for el in data_to_get:
            self._validate_arg(arg_name="data_to_get_el", expected=str, data=el)

        response = await self._db.hmget(key, data_to_get)

        time_to_live = self._unpack_data(await self._db.hget(key, "lifetime"))
        await self._db.expire(key, time_to_live)

        return {
            data_to_get[i]: self._unpack_data(response[i]) for i in range(len(response))
            if response[i] is not None
        }


