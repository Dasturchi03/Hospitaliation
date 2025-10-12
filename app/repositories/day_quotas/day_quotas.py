from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import subqueryload
from app.models.day_quota import DayQuota
from app.models.departments import Department
from app.repositories.departments import departments as rp_dep
from app.services.common import _get_one, _get_all
from app.utils.di.db_ctx import DB


async def _get_or_create_day_quotas(date_: date):
    departments = await _get_all(
        rp_dep._get_departments()
    )

    for dep in departments:
        await _get_or_create_day_quota(date_=date_, department_id=dep.id)

    stmt = select(
        DayQuota
    ).options(
        subqueryload(DayQuota.department)
    ).where(
        DayQuota.date == date_
    )

    return await _get_all(stmt)


async def _get_or_create_day_quota(date_: date, department_id: int):
    qv = await _get_quota(date_=date_, department_id=department_id)

    if not qv:
        department = await rp_dep._get_department(department_id=department_id)
        qv = DayQuota(
            department_id = department_id,
            date = date_,
            base_slots = department.default_quota
        )
        DB.add(qv)
        await DB.flush()
        await DB.refresh(qv)

    return qv


async def _get_quota(date_: date, department_id: int):
    stmt = select(
        DayQuota
    ).where(
        (DayQuota.date == date_) &
        (DayQuota.department_id == department_id)
    )

    return await _get_one(stmt)
