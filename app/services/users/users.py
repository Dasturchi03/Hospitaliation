from app.api.auth.models import Users
from app.repositories.users import users as rp
from app.services.common import _get_all


async def get_user(user_id: int = None, username: str = None) -> Users:
    return await rp._get_user(user_id=user_id, username=username)


async def get_users():
    stmt = await rp._get_users()

    return await _get_all(stmt)
