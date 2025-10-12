import logging
from fastapi import APIRouter
from app.schemas.test import test as sc
from app.services.test import test as sv
from app.utils.deps.auth import Auth


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/test", tags=["Test"]
)


@router.get('/users', response_model=sc.ListUsers)
async def get_users():
    return await sv.get_users()


@router.post('/test')
async def test(request: sc.AddUser):
    return await sv.test(request=request)
