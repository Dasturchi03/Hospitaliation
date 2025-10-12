from typing import List, Optional, Literal, get_args
from datetime import datetime, date as PyDate
from app.schemas.common import BaseSchema, ForDate, Result
from app.schemas.doctors.doctors import DoctorLessOut
from app.schemas.departments.departments import DepartmentOut


AppointmentStatusLiteral = Literal["planned", "admitted", "hospitalized", "canceled"]
AppointmentStatusTuple = get_args(AppointmentStatusLiteral)


class AppointmentBase(BaseSchema):
    department_id: int
    date: PyDate
    slot_no: int
    doctor_id: int

    patient_fullname: Optional[str]
    birth_date: Optional[PyDate]
    diagnosis: Optional[str]
    phone: Optional[str]
    purpose: Optional[str]
    doctor_name_text: Optional[str]

    note_for_head: Optional[str]
    note_public: Optional[str]


class AppointmentAddRequest(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    note_for_head: Optional[str] = None
    created_by_user: Optional[DoctorLessOut] = None
    created_at: datetime
    updated_at: datetime

    department: DepartmentOut
    doctor: Optional[DoctorLessOut] = None


ListAppointments = List[AppointmentOut]
