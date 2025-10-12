from fastapi import APIRouter
from app.services.appointments import appointments as sv
from app.schemas.appointments import appointments as sc
from app.utils.deps.auth import Auth, auth


router = APIRouter(prefix='/appointments', tags=['Appointments'], dependencies=[auth])


@router.get('/get/{appointment_id}', response_model=sc.AppointmentOut)
async def get_appointment(appointment_id: int):
    return await sv.get_appointment(appointment_id=appointment_id)


@router.get('/get-list', response_model=sc.ListAppointments)
async def get_department_appointments(department_id: int, for_date: sc.ForDate):
    return await sv.get_department_appointments(department_id=department_id, date_=for_date)


@router.post('/add-appointment', response_model=sc.Result)
async def add_appointment(request: sc.AppointmentAddRequest, user: Auth):
    return await sv.add_appointment(request=request, user=user)


@router.put('/set-status/{appointment_id}', response_model=sc.Result)
async def set_appointment_status(appointment_id: int, status: sc.AppointmentStatusLiteral):
    return await sv.update_appointment_status(appointment_id=appointment_id, status=status)
