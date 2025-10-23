from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import subqueryload
from app.models.appointments import Appointment
from app.services.common import _get_one
from app.utils.di.db_ctx import DB
from app.utils.exc import NotFoundError


async def _get_appointment(appointment_id: int, raise_: bool = True):
    appointment = await DB.get(Appointment, appointment_id)

    if not appointment:
        if raise_:
            raise NotFoundError("Appointment topilmadi!")

    return appointment


def _get_appointments(department_id: int = None, date_: date = None, status: str = None):

    stmt = select(
        Appointment
    ).options(
        subqueryload(Appointment.department),
        subqueryload(Appointment.doctor),
        subqueryload(Appointment.created_by_user)
    )

    if department_id:
        stmt = stmt.where(
            Appointment.department_id == department_id
        )

    if date_:
        stmt = stmt.where(
            Appointment.date == date_
        )

    if status:
        stmt = stmt.where(
            Appointment.status == status
        )

    return stmt
