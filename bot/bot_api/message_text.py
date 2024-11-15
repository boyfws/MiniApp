from dataclasses import dataclass


@dataclass(frozen=True)
class TextForMessages:
    start: str = "Привет медвед"
    rest_management: str = "Привет, ты перешел на страницу для управления ресторанами"


TEXT = TextForMessages()
