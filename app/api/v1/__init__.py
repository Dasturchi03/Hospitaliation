from fastapi import APIRouter


router_v1 = APIRouter(prefix='/v1')


#routes
from .doctors import doctors
from .departments import departments
from .day_quotas import day_quotas
from .appointments import appointments
from .test import test


router_v1.include_router(departments.router)
router_v1.include_router(doctors.router)
router_v1.include_router(day_quotas.router)
router_v1.include_router(appointments.router)
router_v1.include_router(test.router)
