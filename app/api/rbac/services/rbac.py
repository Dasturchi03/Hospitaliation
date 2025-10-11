from fastapi.routing import APIRoute
from app.utils.di.db_ctx import DB
from app.api.rbac.models import Roles
from app.repositories.users import users as rp_users
from app.api.rbac.repositories import roles as rp_roles
from app.api.rbac.repositories import permissions as rp_permission
from app.api.rbac.schemas import rbac as sc
from app.services.common import _get_all
from app.utils.responses import AddedResponse, UpdatedResponse, DeletedResponse


async def load_routes():
    from app.core.app import app

    tags_map = {}

    for route in app.router.routes:
        if isinstance(route, APIRoute) and route.tags:
            for tag in route.tags:
                tags_map.setdefault(tag, []).append(route.path)

    tags_list = [{"tag": tag, "path": paths} for tag, paths in tags_map.items()]

    await rp_permission._update_permissions(tags_list)

    return UpdatedResponse("Ok")


async def get_roles():
    return await _get_all(
        rp_roles._get_roles()
    )


async def get_permissions(role_id: int = None):
    if role_id:
        await rp_roles._get_role(role_id=role_id)
    stmt = rp_permission._get_permissions(role_id=role_id)

    return await _get_all(stmt)


async def add_role(request: sc.AddRole):
    await rp_roles._get_role_by_name(name=request.name)
    role = Roles(
        name = request.name,
        level = request.level
    )
    DB.add(role)
    await DB.flush()
    await DB.refresh(role)

    return AddedResponse(
        sc.RoleOut.model_validate(role).model_dump(),
        "Role qo'shildi!"
    )


async def update_user_roles(request: sc.UpdateUserRolesRequest):
    user = await rp_users._get_user(user_id=request.user_id)
    await user.awaitable_attrs.roles
    user.roles.clear()
    for role_id in request.role_ids:
        role = await rp_roles._get_role(role_id=role_id)
        user.roles.append(role)
    print(user.roles)
    DB.add(user)
    await DB.flush()

    return UpdatedResponse(message="User rollari yangilandi!")


async def update_role_permissions(request: sc.UpdateRolePermissionsRequest):
    role = await rp_roles._get_role(role_id=request.role_id)
    await role.awaitable_attrs.permissions

    role.permissions.clear()

    for permission_id in request.permission_ids:
        permission = await rp_permission._get_permission(permission_id=permission_id)
        role.permissions.append(permission)

    DB.add(role)
    await DB.flush()

    return UpdatedResponse(message="Role yangilandi!")


async def update_role(role_id: int, request: sc.UpdateRole):
    role = await rp_roles._get_role(role_id=role_id)
    if request.name:
        role.name = request.name
    if request.level:
        role.level = request.level

    DB.add(role)
    await DB.flush()

    return UpdatedResponse(message="Role yangilandi!")


async def delete_role(role_id: int):
    role = await rp_roles._get_role(role_id=role_id)
    await DB.delete(role)

    return DeletedResponse(message="Role o'chirildi!")
