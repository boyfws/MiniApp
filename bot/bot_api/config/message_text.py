from dataclasses import dataclass
from typing import Callable


def get_text_for_rest_mes(name: str,
                          city: str,
                          street: str,
                          house: str) -> str:
    return f"Вы находитесь на странице управления рестораном {name} по адресу\nг.{city} ул.{street} дом.{house}\nОпции:"


@dataclass(frozen=True)
class TextForMessages:
    start: str = "Привет новый  пользователь скоро тут будет новая подпись, но пока что, есть только это"
    rest_management: str = "Привет, ты перешел на страницу для управления ресторанами"
    get_text_for_rest_mes: Callable[[str, str, str, str], str] = get_text_for_rest_mes
    start_init_rest: str = "Вы начали создание ресторана, пока вы находитесь в процессе добавления свойств ресторана прочие кнопки станут некликабельными, сейчас вы сможете выбрать свойтва своих уже сущесвтующих ресторанов, которые будут применены к добавляемому"
    notif_that_buttons_are_unclickable_while_adding_rest = "Прежде чем использовать интерфейс закончите добавление ресторана"


TEXT_FOR_MESSAGES = TextForMessages()
