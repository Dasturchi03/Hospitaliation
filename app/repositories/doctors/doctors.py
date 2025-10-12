from sqlalchemy import select
from app.api.auth.models import Users
from app.models.doctors import Doctor
from app.api.rbac.models import Roles
from app.models.departments import Department
from app.services.common import _execute
from app.utils.di.db_ctx import DB
from app.utils.exc import NotFoundError


def _get_doctors(query: str = None):
    
    stmt = select(
        Doctor.id,
        Users.username,
        Doctor.full_name,
        Doctor.speciality,
        Doctor.department_id,
        Department.name.label('department_name')
    ).join(
        Users, Doctor.user_id == Users.id
    ).join(
        Doctor.department
    ).where(
        Doctor.is_active == True
    )

    if query:
        stmt = stmt.where(
            Doctor.full_name.ilike(f"%{query}%") |
            Users.username.ilike(f"%{query}%") |
            Department.name.ilike(f"%{query}%")
        )

    return stmt


async def _get_doctor_obj(doctor_id: int, raise_: bool = True):
    dr = await DB.get(Doctor, doctor_id)

    if not dr:
        if raise_:
            raise NotFoundError("Doctor mavjud emas!")

    return dr

async def _get_doctor(doctor_id: int):

    stmt = select(
        Doctor.id,
        Users.username,
        Doctor.full_name,
        Doctor.speciality,
        Doctor.department_id,
        Department.name.label('department_name')
    ).join(
        Users, Doctor.user_id == Users.id
    ).join(
        Doctor.department
    ).where(
        Doctor.id == doctor_id
    )

    return (await _execute(stmt))[0]


async def _get_doctor_permissions(doctor_id: int):
    doctor = await DB.get(Doctor, doctor_id)

    if not doctor:
        raise NotFoundError("Foydalanuvchi mavjud emas!")

    user = await doctor.awaitable_attrs.user
    await user.awaitable_attrs.roles

    return user.roles

