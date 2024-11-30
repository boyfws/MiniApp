from src.models.dto.menu import MenuDTO
from tests.test_repository.test_menu import drinks, food


def get_menus() -> tuple[MenuDTO, MenuDTO]:
    menu1 = MenuDTO(
        restaurant_id=1,
        categories=[drinks],
        restaurant_description='ресторан где можно выпить вино и коктейли'
    )
    menu2 = MenuDTO(
        restaurant_id=2,
        categories=[food],
        restaurant_description='бургерная'
    )
    return menu1, menu2