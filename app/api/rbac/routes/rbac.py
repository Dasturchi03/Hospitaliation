from fastapi import APIRouter
from app.api.rbac.schemas import rbac as sc
from app.api.rbac.services import rbac as sv
from app.utils.deps.auth import auth


router = APIRouter(prefix='/rbac', tags=["RBAC"])


@router.get('/')
async def load_routes():
    return await sv.load_routes()


@router.get('/get-permissions', dependencies=[auth], response_model=sc.ListPermissions)
async def get_role_permissions(role_id: int = None):
    return await sv.get_permissions(role_id=role_id)


@router.get('/get-roles', dependencies=[auth], response_model=sc.ListRoles)
async def get_roles():
    return await sv.get_roles()


@router.post('/add-role', dependencies=[auth], response_model=sc.Result)
async def add_role(request: sc.AddRole):
    return await sv.add_role(request=request)


@router.put('/reappend-role', dependencies=[auth], response_model=sc.Result)
async def append_role_to_user(request: sc.UpdateUserRolesRequest):
    return await sv.update_user_roles(request=request)


@router.put('/update-role', dependencies=[auth], response_model=sc.Result)
async def update_role(role_id: int, request: sc.UpdateRole):
    return await sv.update_role(role_id=role_id, request=request)


@router.put('/reappend-role-permissions', dependencies=[auth], response_model=sc.Result)
async def reset_and_append_permissions_to_role(request: sc.UpdateRolePermissionsRequest):
    return await sv.update_role_permissions(request=request)


@router.delete('/delete-role', dependencies=[auth], response_model=sc.Result)
async def delete_role(role_id: int):
    return await sv.delete_role(role_id=role_id)
