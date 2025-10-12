from fastapi import APIRouter
from app.services.departments import departments as sv
from app.schemas.departments import departments as sc
from app.utils.deps.auth import auth


router = APIRouter(prefix='/departments', tags=['Departments'], dependencies=[auth])


@router.get('/get-all', response_model=sc.DepartmentsListOut)
async def get_departments(query: str = None):
    return await sv.get_departments(query=query)


@router.get('/get/{department_id}', response_model=sc.DepartmentOut)
async def get_department(department_id: int):
    return await sv.get_department(department_id=department_id)


@router.post('/add', response_model=sc.Result)
async def add_department(request: sc.AddDepartmentRequest):
    return await sv.add_department(request=request)


@router.put('/update/{department_id}', response_model=sc.Result)
async def update_department(department_id: int, request: sc.UpdateDepartmentRequest):
    return await sv.update_department(department_id=department_id, request=request)


@router.delete('/delete/{department_id}', response_model=sc.Result)
async def delete_department(department_id: int):
    return await sv.delete_department(department_id=department_id)
