from src.models.dto.favourites import FavouriteCategoryDTO, FavouriteCategoryRequest

burgers_1 = FavouriteCategoryDTO(user_id=1, cat_name="Бургеры")
sushi_1 = FavouriteCategoryDTO(user_id=1, cat_name="Суши")
pizza_2 = FavouriteCategoryDTO(user_id=2, cat_name="Пицца")
burgers_2 = FavouriteCategoryDTO(user_id=2, cat_name="Бургеры")

dto_burgers_1 = FavouriteCategoryRequest(user_id=1, cat_id=1)
dto_sushi_1 = FavouriteCategoryRequest(user_id=1, cat_id=2)
dto_pizza_2 = FavouriteCategoryRequest(user_id=2, cat_id=3)
dto_burgers_2 = FavouriteCategoryRequest(user_id=2, cat_id=1)