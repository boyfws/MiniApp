from dataclasses import dataclass


@dataclass(frozen=True)
class NamesForCallback:
    switch_to_rest_management: str = "STRM"
    create_new_rest: str = "CNR"
    start: str = "START"


CallbackNames = NamesForCallback()
