from datetime import date
from app.repositories.day_quotas import day_quotas as rp
from app.services.common import _get_all
from app.utils.di.db_ctx import DB
from app.utils.responses import UpdatedResponse


async def get_todays_quota(date_: date):
    quotas = await rp._get_or_create_day_quotas(date_=date_)

    return quotas


async def add_extra_quotas_for_day(department_id: int, extra_slots: int, date_: date):
    qv = await rp._get_or_create_day_quota(date_=date_, department_id=department_id)

    qv.extra_slots = extra_slots

    await DB.flush()

    return UpdatedResponse(message="Qo'shimcha kvotalar yangilandi!")
