from typing import Callable, Any

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orm.schemas import FavCatForUser
from src.repository.category.category import CategoryRepo


async def add_fav_cat_for_user(session: AsyncSession, cat_id: int, user_id: int) -> None:
    stmt_check = select(FavCatForUser).where(
        FavCatForUser.user_id == user_id,
        FavCatForUser.cat_id == cat_id
    )
    result = await session.execute(stmt_check)
    # если такой категории нет, то добавим
    if not result.scalar_one_or_none():
        stmt = insert(FavCatForUser).values(user_id=user_id, cat_id=cat_id).returning(FavCatForUser.cat_id)
        await session.execute(stmt)

async def extract_name_by_id_for_all_categories(
        session_getter: Callable[[], AsyncSession],
        fav_categories: Any
) -> list[dict[str, str]]:
    cat_repo = CategoryRepo(session_getter=session_getter)
    return [
        {'cat_name': await cat_repo.get_name(cat[0])} for cat in fav_categories.all()
    ]