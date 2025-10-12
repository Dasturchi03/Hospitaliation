from typing import List, Optional
from app.schemas.common import BaseSchema, Result
from app.api.rbac.schemas.rbac import RolePermissions


class DoctorBase(BaseSchema):
    username: str
    full_name: str
    department_id: int
    speciality: str


class AddDoctorRequest(DoctorBase):
    password: str


class DoctorOut(DoctorBase):
    id: int
    username: str
    full_name: str
    speciality: str
    department_id: int
    department_name: str


class UserUsername(BaseSchema):
    username: str


class DoctorLessOut(BaseSchema):
    id: int
    full_name: str
    user: UserUsername


class DoctorFullOut(BaseSchema):
    doctor: DoctorOut
    roles: List[RolePermissions]


class UpdateDoctorRequest(AddDoctorRequest):
    full_name: Optional[str] = None
    department_id: Optional[int] = None
    speciality: Optional[str] = None
    password: Optional[str] = None


ListDoctors = List[DoctorOut]
