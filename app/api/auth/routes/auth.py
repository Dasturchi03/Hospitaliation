import logging
from fastapi import APIRouter
from app.api.auth.schemas import user_auth as sc
from app.api.auth.services import user_auth as sv


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/auth", tags=["Auth"]
)


@router.post('/login')
async def login_user(request: sc.UserLoginRequest):
    return await sv.login_user(request=request)
