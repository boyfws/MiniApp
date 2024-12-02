from bot_api.callback_handlers.Message import StartMessage, RestManageMessage
from bot_api.callback_handlers.Utils import CommonTools


class CallBackHandlers(StartMessage,
                        RestManageMessage,
                        CommonTools):
    def __init__(self):
        super().__init__()
