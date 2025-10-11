from fastapi import APIRouter


router_v1 = APIRouter(prefix='/v1')


#routes
from .test import test


router_v1.include_router(test.router)
