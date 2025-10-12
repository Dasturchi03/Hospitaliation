from datetime import date
from app.schemas.appointments import appointments as sc
from app.services.common import _get_all
from app.repositories.appointments import appointments as rp
from app.repositories.departments import departments as rp_dep
from app.models.appointments import Appointment
from app.api.auth.models.users import Users
from app.utils.di.db_ctx import DB
from app.utils.responses import AddedResponse, UpdatedResponse


async def get_appointment(appointment_id: int):
    appointment = await rp._get_appointment(appointment_id=appointment_id)

    await appointment.awaitable_attrs.doctor
    await appointment.awaitable_attrs.department
    await appointment.awaitable_attrs.created_by_user

    return appointment


async def get_department_appointments(department_id: int, date_: date):
    await rp_dep._get_department(department_id=department_id)
    stmt = rp._get_appointments(
        department_id=department_id,
        date_=date_
    )

    return await _get_all(stmt)


async def add_appointment(request: sc.AppointmentAddRequest, user: Users):
    await user.awaitable_attrs.doctors

    appointment = Appointment(
        **request.model_dump()
    )
    appointment.created_by = user.doctors[0].id if user.doctors else None
    DB.add(appointment)
    await DB.flush()
    await DB.refresh(appointment)
    await appointment.awaitable_attrs.created_by_user
    await appointment.awaitable_attrs.department
    await appointment.awaitable_attrs.doctor
    await appointment.doctor.awaitable_attrs.user

    return AddedResponse(
        data=sc.AppointmentOut.model_validate(appointment),
        message="Appointment qo'shildi!"
    )


async def update_appointment_status(appointment_id: int, status: sc.AppointmentStatusLiteral):
    appointment = await rp._get_appointment(appointment_id=appointment_id)

    old_status = appointment.status
    appointment.status = status

    await DB.flush()

    return UpdatedResponse(message=f"Appointment statusi {old_status} dan {appointment.status} ga o'zgardi!")
