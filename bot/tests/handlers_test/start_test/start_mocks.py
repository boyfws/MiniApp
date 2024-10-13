from telegram import MenuButtonWebApp, InlineKeyboardMarkup
import telegram
from typing import List, Tuple
from telegram import Message
import asyncio
import random

MAX_DELAY_IN_SEC = 0.1


# Задаем макс кол-во секунд, которое может быть потрачено для обращения к серверу

# Mock for User (with extra method get)
class User:
    def __init__(self, id: int, language_code: str) -> None:
        self.id: int = id
        """
        lang_code:
        IETF language tag of the user’s language.
        """
        self.language_code = language_code
        self.messages: List[Tuple[str, InlineKeyboardMarkup]] = []

    def get_message(self, data_to_add: Tuple[str, InlineKeyboardMarkup]) -> None:
        self.messages.append(data_to_add)


# Mock for Bot
class Bot:
    def __init__(self, broken: bool = False, maximum_number_of_bad_requests: int = 5) -> None:
        """
        Параметр bad отвечает за то, возникнет ли ошибка при обращении к api
        Параметр maximum_number_of_bad_requests отвечает за  количество запросов которые будут сломаны
        Чреез maximum_number_of_bad_requests запрос выполнится
        """
        self.broken = broken
        self.maximum_number_of_bad_requests = maximum_number_of_bad_requests
        self.chats: List["Chat"] = []

    def add_chat(self, data_to_add: "Chat") -> None:
        self.chats.append(data_to_add)

    async def set_chat_menu_button(self, chat_id, menu_button) -> bool | None:
        await asyncio.sleep(random.random() * MAX_DELAY_IN_SEC)  # Имитиация задержки при обращении к API TG
        """
        On success, True is returned
        """
        if self.broken:
            self.maximum_number_of_bad_requests -= 1
            if not self.maximum_number_of_bad_requests:
                self.broken = False
            return None

        for el in self.chats:
            if el.id == chat_id:
                el.add_button(menu_button)
                return True
        return None


# Mock for Message
class Message():
    def __init__(self, from_user: "User", broken: bool = False, maximum_number_of_bad_requests: int = 5) -> None:
        """
        from_user:
        Sender of the message; may be empty for messages sent to channels. For backward compatibility,
        if the message was sent on behalf of a chat, the field contains a fake sender user in non-channel chats.
        """
        self.from_user: "User" = from_user
        self.broken: bool = broken
        self.maximum_number_of_bad_requests: int = maximum_number_of_bad_requests

    async def reply_text(self, reply_text, reply_markup=None) -> Message | None:
        await asyncio.sleep(random.random() * MAX_DELAY_IN_SEC)  # Имитиация задержки при обращении к API TG
        """
        return class:`telegram.Message`: On success, the sent message is returned
        """
        if self.broken:
            self.maximum_number_of_bad_requests -= 1
            if not self.maximum_number_of_bad_requests:
                self.broken = False
            return None

        self.from_user.get_message((reply_text, reply_markup))
        return Message(from_user=telegram.User(id=1, first_name="Test", is_bot=False))


# Mock for Chat
class Chat:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.buttons: List[MenuButtonWebApp] = []

    def add_button(self, data_to_add: MenuButtonWebApp) -> None:
        self.buttons.append(data_to_add)


# Mock for Update
class Update:
    def __init__(self, message: Message, effective_chat: Chat | None) -> None:
        self.message: "Message" = message
        """
        effective_chat:
        The chat that this update was sent in, no matter what kind of update this is. 
        If no chat is associated with this update, this gives None. This is the case, 
        if inline_query, chosen_inline_result, callback_query from inline messages, 
        shipping_query, pre_checkout_query, poll, poll_answer, business_connection, 
        or purchased_paid_media is present.
        """
        self.effective_chat: Chat | None = effective_chat


# Mock for CallbackContext
class CallbackContext:
    def __init__(self, bot: "Bot") -> None:
        self.bot: "Bot" = bot
