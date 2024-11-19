from dataclasses import dataclass


@dataclass(frozen=True)
class NamesForCallback:
    switch_to_rest_management: str = "STRM"
    create_new_rest: str = "CNR"
    start: str = "START"
    block: str = "BLOCK"
    show_rest_info: str = "SRI"
    stop_rest_adding: str = "SRA"


# Кнопки связанные с ресторанами передаются в формате callback:id
# Блокирующие действия передаются в формате callback:BLOCK

# Блокирующие действия - действия при обнаружении которых мы не даем нажимать другие кнопки

CallbackNames = NamesForCallback()
