from fastapi import APIRouter, Query
from app.services.day_quotas import day_quotas as sv
from app.schemas.day_quotas import day_quotas as sc
from app.utils.deps.auth import auth


router = APIRouter(prefix='/day-quota', tags=['Daily quotas API'], dependencies=[auth])


@router.get('/get', response_model=sc.ListDayQuotas)
async def get_todays_quota(for_date: sc.ForDate):
    return await sv.get_todays_quota(date_=for_date)


@router.put('/add-extra-quota', response_model=sc.Result)
async def add_extra_quota_for_date(department_id: int, extra_slots: int, for_date: sc.ForDate):
    return await sv.add_extra_quotas_for_day(date_=for_date, department_id=department_id, extra_slots=extra_slots)
