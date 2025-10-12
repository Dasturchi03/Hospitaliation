from typing import List, Optional
from app.schemas.common import BaseSchema, Result


class DepartmentBase(BaseSchema):
    name: str
    default_quota: int
    is_active: bool


class AddDepartmentRequest(BaseSchema):
    name: str
    default_quota: int


class DepartmentOut(DepartmentBase):
    id: int


class UpdateDepartmentRequest(DepartmentBase):
    name: Optional[str] = None
    default_quota: Optional[int] = None
    is_active: Optional[bool] = None


DepartmentsListOut = List[DepartmentOut]
