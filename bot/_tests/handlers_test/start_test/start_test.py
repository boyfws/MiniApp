import pytest
import asyncio
from typing import Tuple, Union

from bot.handlers.start_command import *
from start_mocks import *


def get_all_obj(lang_code: str,
                message_broken: bool = False,
                bot_broken: bool = False,
                max_bad_req_mes: int = 2,
                max_bad_req_bot: int = 2,
                n_users: int = 1
                ) -> Tuple[
    Bot,
    CallbackContext,
    Union[User, List[User]],
    Union[Chat, List[Chat]],
    Union[Update, List[Update]]
]:
    bot = Bot(broken=bot_broken, maximum_number_of_bad_requests=max_bad_req_bot)
    context = CallbackContext(bot)

    users = []
    chats = []
    updates = []
    for i in range(n_users):
        user_to_add = User(i, language_code=lang_code)
        chat_to_add = Chat(i)

        bot.add_chat(chat_to_add)

        users.append(user_to_add)
        chats.append(chat_to_add)
        updates.append(Update(Message(user_to_add, broken=message_broken,
                                      maximum_number_of_bad_requests=max_bad_req_mes),
                              effective_chat=chat_to_add))

    if n_users == 1:
        users = users[0]
        chats = chats[0]
        updates = updates[0]
    return bot, context, users, chats, updates


@pytest.fixture()
def add_mocks():
    return get_all_obj


@pytest.mark.parametrize("lang_code, exp_code, expected_button, expected_keyboard", [
    ("ru", "ru", menu_bottom_miniapp_ru, start_keyboard_ru),
    ("en", "en", menu_bottom_miniapp_en, start_keyboard_en),
    ("da", "ru", menu_bottom_miniapp_ru, start_keyboard_ru)
])
def test_normal_requests(lang_code: str, exp_code: str, expected_button: MenuButtonWebApp,
                         expected_keyboard: InlineKeyboardMarkup, add_mocks) -> None:
    """
    Проверяем, что польз с англ, яз получит сообщение на английском, с русским или неизв - на русском

    """
    bot, context, user, chat, update = add_mocks(lang_code, False, False, n_users=1)
    asyncio.run(start(update, context))

    assert user.messages == [(lang_of_response_text[exp_code], expected_keyboard)]
    assert chat.buttons == [expected_button]


@pytest.mark.asyncio
@pytest.mark.parametrize("lang_code, exp_code, expected_button, expected_keyboard", [
    ("ru", "ru", menu_bottom_miniapp_ru, start_keyboard_ru),
    ("en", "en", menu_bottom_miniapp_en, start_keyboard_en),
    ("da", "ru", menu_bottom_miniapp_ru, start_keyboard_ru)
])
async def test_multiple_requests(lang_code: str, exp_code: str, expected_button: MenuButtonWebApp,
                                 expected_keyboard: InlineKeyboardMarkup, add_mocks) -> None:
    """
    Много пользователей пытаются обратиться к системе
    """
    n_users = 10

    bot, context, users, chats, updates = add_mocks(lang_code, False, False, n_users=n_users)

    await asyncio.gather(*(start(updates[i], context) for i in range(n_users)))

    for i in range(n_users):
        assert users[i].messages == [(lang_of_response_text[exp_code], expected_keyboard)]
        assert chats[i].buttons == [expected_button]


@pytest.mark.parametrize("lang_code, exp_code, expected_button, expected_keyboard", [
    ("ru", "ru", menu_bottom_miniapp_ru, start_keyboard_ru),
    ("en", "en", menu_bottom_miniapp_en, start_keyboard_en),
    ("da", "ru", menu_bottom_miniapp_ru, start_keyboard_ru)
])
def test_mistake_in_message_send(lang_code: str, exp_code: str, expected_button: MenuButtonWebApp,
                                 expected_keyboard: InlineKeyboardMarkup, add_mocks) -> None:
    """
    Возникала ошибка при отправке сообщения

    """
    bot, context, user, chat, update = add_mocks(lang_code, True, False, max_bad_req_mes=3, n_users=1)

    asyncio.run(start(update, context))

    assert user.messages == [(lang_of_response_text[exp_code], expected_keyboard)]
    assert chat.buttons == [expected_button]


@pytest.mark.parametrize("lang_code, exp_code, expected_button, expected_keyboard", [
    ("ru", "ru", menu_bottom_miniapp_ru, start_keyboard_ru),
    ("en", "en", menu_bottom_miniapp_en, start_keyboard_en),
    ("da", "ru", menu_bottom_miniapp_ru, start_keyboard_ru)
])
def test_mistake_in_button_send(lang_code: str, exp_code: str, expected_button: MenuButtonWebApp,
                                expected_keyboard: InlineKeyboardMarkup, add_mocks) -> None:
    """
    Возникала ошибка при установке кнопки

    """
    bot, context, user, chat, update = add_mocks(lang_code, False, True, max_bad_req_bot=3, n_users=1)

    asyncio.run(start(update, context))

    assert user.messages == [(lang_of_response_text[exp_code], expected_keyboard)]
    assert chat.buttons == [expected_button]


@pytest.mark.parametrize("lang_code, exp_code, expected_button, expected_keyboard", [
    ("ru", "ru", menu_bottom_miniapp_ru, start_keyboard_ru),
    ("en", "en", menu_bottom_miniapp_en, start_keyboard_en),
    ("da", "ru", menu_bottom_miniapp_ru, start_keyboard_ru)
])
def test_mistake_in_button_and_message_send(lang_code: str, exp_code: str, expected_button: MenuButtonWebApp,
                                            expected_keyboard: InlineKeyboardMarkup, add_mocks) -> None:
    """
    Возникала ошибка и при установке кнопки и при отправке сообщения

        """
    bot, context, user, chat, update = add_mocks(lang_code, True, True,
                                                 max_bad_req_bot=3, max_bad_req_mes=3, n_users=1)

    asyncio.run(start(update, context))

    assert user.messages == [(lang_of_response_text[exp_code], expected_keyboard)]
    assert chat.buttons == [expected_button]
