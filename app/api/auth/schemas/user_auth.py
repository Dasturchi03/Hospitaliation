from typing import List
from app.schemas.common import BaseSchema
from app.api.rbac.schemas.rbac import PermissionOut


class UserOut(BaseSchema):
    id: int
    username: str


class UserLoginRequest(BaseSchema):
    username: str
    password: str


class UserLoggedIn(BaseSchema):
    token: str
    user: UserOut
    permissions: List[PermissionOut]
