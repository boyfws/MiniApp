from dataclasses import dataclass


@dataclass(frozen=True)
class NamesForCallback:
    switch_to_rest_management: str = "STRM"
    create_new_rest: str = "CNR"
    start: str = "START"
    block: str = "BLOCK"
    show_rest_info: str = "SRI"
    stop_rest_adding: str = "SRA"
    adding_rest_conv_mark: str = "ARCV"
    inheritance_property_of_rest: str = "IPOR"
    switch_from_inheritance: str = "SFI"



"""
Колбэки передаются в формате {conv_mark + _}{callback}:{extra_args}
conv_mark позволяет отделить нажатия кнопок в рамках одного conversation от других, conv_mark - опциональный аргумент
"""
CallbackNames = NamesForCallback()
