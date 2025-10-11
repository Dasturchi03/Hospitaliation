from sqlalchemy import select
from app.services.common import _get_one
from app.api.rbac.models import PermissionCategory, Permissions, Roles
from app.services.common import _get_one
from app.utils.di.db_ctx import DB
from app.utils.exc import NotFoundError


async def _update_permissions(tags_list: list[dict]):
    for dc in tags_list:
        tag, paths = dc['tag'], dc['path']
        category = await _get_or_create_category(tag)
        await category.awaitable_attrs.endpoints
        category.endpoints.clear()

        DB.add(category)
        await DB.flush()

        for endpoint in paths:
            permission = await _get_or_create_permission(endpoint)
            category.endpoints.append(permission)
            DB.add(category)
            await DB.flush()


async def _get_or_create_category(category_name: str):

    stmt = select(
        PermissionCategory
    ).where(
        PermissionCategory.name == category_name
    )

    category = await _get_one(stmt)

    if not category:
        category = PermissionCategory(
            name=category_name
        )
        DB.add(category)
        await DB.flush()

    return category


async def _get_or_create_permission(endpoint: str):

    stmt = select(
        Permissions
    ).where(
        Permissions.endpoint == endpoint
    )

    permission = await _get_one(stmt)

    if not permission:
        permission = Permissions(
            name=endpoint,
            endpoint=endpoint
        )
        DB.add(permission)
        await DB.flush()

    return permission


async def _get_permission(permission_id: int, raise_: bool = True):
    permission = await DB.get(Permissions, permission_id)

    if raise_:
        if not permission:
            raise NotFoundError("Permission mavjud emas!")

    return permission


def _get_permissions(role_id: int = None):

    stmt = select(Permissions)

    if role_id:
        stmt = stmt.where(
            Permissions.roles.any(Roles.id == role_id)
        )

    stmt = stmt.order_by(
        Permissions.category_id
    )

    return stmt
