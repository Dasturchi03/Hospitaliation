from sqlalchemy import select
from app.services.common import _get_one
from app.api.rbac.models import Roles
from app.utils.exc import NotFoundError, HasAnyError
from app.utils.di.db_ctx import DB


def _get_roles():
    stmt = select(Roles)
    return stmt


async def _get_role(role_id: int, raise_: bool = True):
    role = await DB.get(Roles, role_id)

    if raise_:
        if not role:
            raise NotFoundError("Role mavjud emas!")

    return role


async def _get_role_by_name(name: str, raise_if_exists: bool = True):
    stmt = select(
        Roles
    ).where(
        Roles.name == name
    )

    role = await _get_one(stmt)

    if role:
        if raise_if_exists:
            raise HasAnyError("Bunday role mavjud!")

    return role
