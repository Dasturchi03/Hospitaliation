from sqlalchemy import select
from app.models.departments import Department
from app.services.common import _get_one
from app.utils.di.db_ctx import DB
from app.utils.exc import NotFoundError


def _get_departments(query: str = None, is_active: bool = True):
    stmt = select(Department).where(
        Department.is_active == is_active
    )

    if query:
        stmt.where(
            Department.name.ilike(f"%{query}%")
        )

    return stmt


async def _get_department(department_id: int, raise_: bool = True):
    department = await DB.get(Department, department_id)

    if not department:
        if raise_:
            raise NotFoundError("Bo'lim | Department topilmadi!")

    return department
