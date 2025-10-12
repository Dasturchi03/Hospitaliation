from typing import List
from datetime import datetime, date as PyDate
from app.schemas.departments.departments import DepartmentOut
from app.schemas.common import BaseSchema, ForDate, Result


class DayQuotaBase(BaseSchema):
    id: int
    department_id: int
    date: PyDate
    base_slots: int
    extra_slots: int
    updated_at: datetime
    department: DepartmentOut


ListDayQuotas = List[DayQuotaBase]
