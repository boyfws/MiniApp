import pytest
import asyncio
from typing import Union
import os

from bot.handlers.start_command import *
from start_mocks import *


def run_tests():
    command = "pytest"
    os.system(command)


def get_all_obj(message_broken: bool = False,
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
        user_to_add = User(i)
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


@pytest.fixture(scope="function")
def add_mocks():
    return get_all_obj


def test_normal_requests(add_mocks) -> None:
    """
    Проверка базовой работы бота
    """
    bot, context, user, chat, update = add_mocks(False, False, n_users=1)
    asyncio.run(start(update, context))

    assert user.messages == [(response_text, start_keyboard)]
    assert chat.buttons == [menu_bottom_miniapp]


@pytest.mark.asyncio
async def test_multiple_requests(add_mocks) -> None:
    """
    Много пользователей пытаются обратиться к системе
    """
    n_users = 10

    bot, context, users, chats, updates = add_mocks(False, False, n_users=n_users)

    await asyncio.gather(*(start(updates[i], context) for i in range(n_users)))

    for i in range(n_users):
        assert users[i].messages == [(response_text, start_keyboard)]
        assert chats[i].buttons == [menu_bottom_miniapp]


@pytest.mark.parametrize("message_broken, bot_broken, max_bad_req_mes, max_bad_req_bot", [
    (True, False, 3, None),
    (False, True, None, 3),
    (True, True, 3, 3)
], ids=(
        "Возникла ошибка при отправке соощения",
        "Возникла ошибка при отправе кнопки боту",
        "Возникла ошибка при отправке сообщения и при отправке кнопки"

))
def test_mistake_in_message_send(message_broken,
                                 bot_broken,
                                 max_bad_req_mes,
                                 max_bad_req_bot,
                                 add_mocks) -> None:
    """
    Возникла какаая либо ошибка
    """
    bot, context, user, chat, update = add_mocks(message_broken=message_broken,
                                                 bot_broken=bot_broken,
                                                 max_bad_req_mes=max_bad_req_mes,
                                                 max_bad_req_bot=max_bad_req_bot,
                                                 n_users=1)
    asyncio.run(start(update, context))

    assert user.messages == [(response_text, start_keyboard)]
    assert chat.buttons == [menu_bottom_miniapp]


if __name__ == "__main__":
    run_tests()