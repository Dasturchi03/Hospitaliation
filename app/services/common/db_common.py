from typing import Tuple, TypeVar, Sequence, Optional
from sqlalchemy.sql.selectable import Select
from app.utils.di.db_ctx import DB


_T = TypeVar("_T")


async def _get_one(stmt: Select[Tuple[_T]]) -> Optional[_T]:
    return (await DB.execute(stmt)).unique().scalar_one_or_none()


async def _get_all(stmt: Select[Tuple[_T]]) -> Sequence[_T]:
    return (await DB.execute(stmt)).unique().scalars().all()


async def _execute(stmt: Select[Tuple[_T]]) -> Sequence[_T]:
    return (await DB.execute(stmt)).all()
