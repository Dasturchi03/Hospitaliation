from sqlalchemy import select
from app.api.auth.models import Users
from app.utils.exc import NotFoundError
from app.services.common import _get_one


async def _get_user(user_id: int = None, username: str = None) -> Users:
    stmt = select(Users)

    if user_id:
        stmt = stmt.where(
            Users.id == user_id
        )
    elif username:
        stmt = stmt.where(
            Users.username == username
        )
    user = await _get_one(stmt)

    if not user:
        raise NotFoundError(404, "User not found!")

    return user


async def _get_users():
    stmt = select(Users)

    return stmt
