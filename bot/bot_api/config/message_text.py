from dataclasses import dataclass
from typing import Callable

from .callback_names import PropInCallBack_INH


def get_text_for_rest_mes(name: str,
                          city: str,
                          street: str,
                          house: str) -> str:
    return f"Вы находитесь на странице управления рестораном {name} по адресу\nг.{city} ул.{street} дом.{house}\nОпции:"


def get_text_for_rest_mes_inheritance(name: str) -> str:
    return f"Вы находитесь на странице ресторана {name} выберите свойства данного ресторана, которые вы хотите применить к создаваемому ресторану"


def get_text_for_mes_show_confirm_inh(prop_callback: str, rest_name: str) -> str:
    conv_dict = {
        PropInCallBack_INH.description: "Описание",
        PropInCallBack_INH.website: "Ссылка на сайт",
        PropInCallBack_INH.ext_serv_1: "Ссылка на внешний сервис 1",
        PropInCallBack_INH.ext_serv_2: "Ссылка на внешний сервис 2",
        PropInCallBack_INH.ext_serv_3: "Ссылка на внешний сервис 3",
        PropInCallBack_INH.tg_link: "Ссылка на телеграм",
        PropInCallBack_INH.inst_link: "Ссылка на инстаграм",
        PropInCallBack_INH.vk_link: "Ссылка на вк",
        PropInCallBack_INH.orig_phone: "Номер телефона",
        PropInCallBack_INH.wapp_phone: "Номер телефона для wapp",
        PropInCallBack_INH.menu: "Меню",
        PropInCallBack_INH.categories: "Категории"
    }
    return f'Вы находитесь на странице добавления свойства "{conv_dict[prop_callback]}" из вашего ресторана {rest_name}. Вы можете применить данное свойство или отобразить его'



@dataclass(frozen=True)
class DynamicTextForMessages:
    get_text_for_rest_mes: Callable[[str, str, str, str], str] = get_text_for_rest_mes
    get_text_for_rest_mes_inheritance: Callable[[str], str] = get_text_for_rest_mes_inheritance
    get_text_for_mes_with_show_confirm: Callable[[str, str], str] = get_text_for_mes_show_confirm_inh



@dataclass(frozen=True)
class TextForMessages(DynamicTextForMessages):
    start: str = "Привет новый  пользователь скоро тут будет новая подпись, но пока что, есть только это"
    rest_management: str = "Привет, ты перешел на страницу для управления ресторанами"
    start_init_rest: str = "Вы начали создание ресторана, пока вы находитесь в процессе добавления свойств ресторана прочие кнопки станут некликабельными, сейчас вы сможете выбрать свойтва своих уже сущесвтующих ресторанов, которые будут применены к добавляемому"
    notif_that_buttons_are_unclickable_while_adding_rest: str = "Прежде чем использовать интерфейс закончите добавление ресторана"


