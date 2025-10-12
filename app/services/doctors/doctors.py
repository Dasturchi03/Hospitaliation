from app.api.auth.models import Users
from app.models.doctors import Doctor
from app.schemas.doctors import doctors as sc
from app.repositories.doctors import doctors as rp
from app.repositories.departments import departments as rp_dep
from app.utils.auth.auth import AuthHandler
from app.services.common import _get_all, _execute
from app.utils.di.db_ctx import DB
from app.utils.responses import AddedResponse, UpdatedResponse, DeletedResponse


async def get_doctors(query: str = None):
    stmt = rp._get_doctors(query=query)

    return await _execute(stmt)


async def get_doctor(doctor_id: int):
    doctor = await rp._get_doctor(doctor_id=doctor_id)
    roles = await rp._get_doctor_permissions(doctor_id=doctor_id)

    return {
        "doctor": doctor,
        "roles": roles
    }


async def add_doctor(request: sc.AddDoctorRequest):
    user = Users(
        username = request.username,
        password = AuthHandler.get_password_hash(request.password)
    )

    DB.add(user)
    await DB.flush()
    await DB.refresh(user)

    dr = Doctor(
        id = user.id,
        user_id = user.id,
        full_name = request.full_name,
        department_id = request.department_id,
        speciality = request.speciality
    )

    DB.add(dr)
    await DB.flush()
    await DB.refresh(dr)

    return AddedResponse(
        data={"id": dr.id},
        message="Doctor qo'shildi"
    )


async def update_doctor(doctor_id: int, request: sc.UpdateDoctorRequest):
    dr = await rp._get_doctor_obj(doctor_id=doctor_id)
    user = await dr.awaitable_attrs.user

    if request.full_name:
        dr.full_name = request.full_name
    if request.department_id:
        dep = await rp_dep._get_department(department_id=request.department_id)
        dr.department_id = dep.id
    if request.speciality:
        dr.speciality = request.speciality
    if request.password:
        user.password = AuthHandler.get_password_hash(request.password)

    await DB.flush()

    return UpdatedResponse(message="Doctor ma'lumotlari yangilandi!")


async def delete_doctor(doctor_id: int):
    dr = await rp._get_doctor_obj(doctor_id=doctor_id)
    dr.is_active = False
    user = await dr.awaitable_attrs.user
    await DB.delete(user)
    await DB.flush()

    return DeletedResponse(message="Doctor o'chirildi")
