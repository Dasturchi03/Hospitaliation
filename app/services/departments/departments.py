from app.models.departments import Department
from app.repositories.departments import departments as rp
from app.schemas.departments import departments as sc
from app.services.common import _get_all
from app.utils.di.db_ctx import DB
from app.utils.responses import AddedResponse, DeletedResponse, UpdatedResponse


async def get_departments(query: str = None):
    stmt = rp._get_departments(query=query, is_active=True)

    return await _get_all(stmt)


async def get_department(department_id: int):
    department = await rp._get_department(department_id=department_id)

    return department


async def add_department(request: sc.AddDepartmentRequest):
    
    department = Department(
        name = request.name,
        default_quota = request.default_quota,
        is_active = True
    )

    DB.add(department)
    await DB.flush()

    return AddedResponse(message="Department qo'shildi!")


async def update_department(department_id: int, request: sc.UpdateDepartmentRequest):
    
    department = await rp._get_department(department_id=department_id)
    if request.name:
        department.name = request.name
    if request.is_active:
        department.is_active = request.is_active
    if request.default_quota:
        department.default_quota = request.default_quota

    await DB.flush()
    await DB.refresh(department)

    return UpdatedResponse(
        data=sc.DepartmentOut.model_validate(department),
        message="Department ma'lumotlari yangilandi!"
    )


async def delete_department(department_id: int):
    department = await rp._get_department(department_id=department_id)

    await DB.delete(department)
    await DB.flush()

    return DeletedResponse(message="Department o'chirildi!")
