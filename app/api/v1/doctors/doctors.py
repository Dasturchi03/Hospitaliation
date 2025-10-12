from fastapi import APIRouter
from app.services.doctors import doctors as sv
from app.schemas.doctors import doctors as sc
from app.utils.deps.auth import auth


router = APIRouter(prefix='/doctors', tags=['Doctors | Site Users'])


@router.get('/get-all', response_model=sc.ListDoctors)
async def get_doctors(query: str = None):
    return await sv.get_doctors(query=query)


@router.get('/get/{doctor_id}', response_model=sc.DoctorFullOut)
async def get_doctor(doctor_id: int):
    return await sv.get_doctor(doctor_id=doctor_id)


@router.post('/add', response_model=sc.Result)
async def add_doctor(request: sc.AddDoctorRequest):
    return await sv.add_doctor(request=request)


@router.put('/update/{doctor_id}', response_model=sc.Result)
async def update_doctor(doctor_id: int, request: sc.UpdateDoctorRequest):
    return await sv.update_doctor(doctor_id=doctor_id, request=request)


@router.delete('/delete/{doctor_id}', response_model=sc.Result)
async def delete_doctor(doctor_id: int):
    return await sv.delete_doctor(doctor_id=doctor_id)
