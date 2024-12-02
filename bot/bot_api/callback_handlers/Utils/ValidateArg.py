from telegram import CallbackQuery
from typing import List

from .Logger import Logger


class ValidateArg(Logger):
    def __init__(self):
        pass

    @staticmethod
    def get_args(query: CallbackQuery) -> List[str]:
        callback, arg = query.data.split(":")
        return arg.split(",")

    def validate_args(self,
                      args: List[str],
                      num_args: int,
                      dtypes: List[type],
                      user_id: int) -> bool:
        # mypy: len(elements) == num_args
        """
        Валидирует полученные в callback аргументы, проверяется количество
        аргументов и их типы данных, возвращает True если все в порядке
        False иначе
        """
        if len(args) != len(dtypes):
            raise ValueError

        if len(args) != num_args:
            return False

        for arg, dtype in zip(args, dtypes):
            try:
                _ = dtype(arg)
            except ValueError:
                self._log_arg_validation_error(user_id=user_id, arg=arg, dtype=dtype)
                return False

        return True
