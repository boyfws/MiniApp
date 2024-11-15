from dataclasses import dataclass


@dataclass(frozen=True)
class TextForButtons:
    link_to_miniapp_text: str = "Наше приложение"
    switch_to_rest_management: str = "Добавить свой ресторан"
    menu_button: str = "Что-то"
    back: str = "Назад"
    create_new_rest: str = "Добавить новый ресторан"


TEXT = TextForButtons()
