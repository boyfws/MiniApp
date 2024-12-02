from dataclasses import dataclass


@dataclass(frozen=True)
class TextForButtons_callback:
    description: str = "Описание"
    main_photo: str = "Главное фото"
    photos: str = "Фото"
    website: str = "Сайт"
    ext_serv_1: str = "Ссылка на сервис 1"
    ext_serv_2: str = "Ссылка на сервис 2"
    ext_serv_3: str = "Ссылка не сервис 3"
    tg_link: str = "Ссылка на Tg"
    inst_link: str = "Ссылка на instagram"
    vk_link: str = "Ссылка на VK"
    orig_phone: str = "Номер телефона"
    wapp_phone: str = "Номер телефона для WatsUpp"
    menu: str = "Меню"
    categories: str = "Категории"


@dataclass(frozen=True)
class TextForButtons(TextForButtons_callback):
    link_to_miniapp_text: str = "Наше приложение"
    switch_to_rest_management: str = "Управление ресторанами"
    menu_button: str = "Что-то"
    create_new_rest: str = "Добавить новый ресторан"
    back_to_message: str = "Вернуться сюда"
    stop_rest_adding: str = "Отменить и удалить все"
    switch_from_inheritance: str = "Продолжить"
    confirm_inheritance: str = "Применить данное свойство"
    show_prop_for_inheritance: str = "Посмотреть"



