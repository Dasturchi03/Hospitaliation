from __future__ import annotations

from typing import List, Optional
from app.schemas.common import BaseSchema, Result


class RoleBase(BaseSchema):
    name: str
    level: int


class AddRole(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int


class UpdateUserRolesRequest(BaseSchema):
    user_id: int
    role_ids: List[int]


class UpdateRolePermissionsRequest(BaseSchema):
    role_id: int
    permission_ids: List[int]


class RolePermissions(RoleBase):
    permissions: List[PermissionOut]


class UpdateRole(RoleBase):
    name: Optional[str] = None
    level: Optional[int] = None


class BasePermission(BaseSchema):
    name: str
    endpoint: str


class PermissionOut(BasePermission):
    id: int


class AddPermission(BasePermission):
    role_id: int


ListPermissions = List[PermissionOut]
ListRoles = List[RoleOut]
