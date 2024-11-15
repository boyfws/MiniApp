from dataclasses import dataclass


@dataclass(frozen=True)
class NamesForCallback:
    switch_to_rest_management: str = "STRM"
    back_from_rest_man: str = "BFRM"
    create_new_rest: str = "CNR"


CallbackNames = NamesForCallback()
