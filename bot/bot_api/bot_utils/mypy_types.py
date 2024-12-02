from telegram import Update, CallbackQuery, Chat, User, InlineKeyboardMarkup, Message

class User_mod(User):
    id: int


class Message_mod(Message):
    reply_markup: InlineKeyboardMarkup
    from_user: User_mod


class CallbackQuery_mod(CallbackQuery):
    data: str
    message: Message_mod


class Chat_mod(Chat):
    id: int


class Update_mod(Update):
    callback_query: CallbackQuery_mod
    effective_chat: Chat_mod
    effective_user: User_mod
    message: Message_mod
