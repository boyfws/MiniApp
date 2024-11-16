from dataclasses import dataclass
from typing import Callable


def get_text_for_rest_mes(name: str,
                          city: str,
                          street: str,
                          house: str) -> str:
    return \
        f"""
    Вы находитесь на странице управления рестораном {name} по адресу\nг.{city} ул.{street} дом.{house}\nОпции: 
        """


@dataclass(frozen=True)
class TextForMessages:
    start: str = "Привет медвед"
    rest_management: str = "Привет, ты перешел на страницу для управления ресторанами"
    get_text_for_rest_mes: Callable[[str, str, str, str], str] = get_text_for_rest_mes


TEXT_FOR_MESSAGES = TextForMessages()
