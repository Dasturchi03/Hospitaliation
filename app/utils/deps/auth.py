from typing import Annotated, TYPE_CHECKING
from fastapi import Depends
from app.utils.auth.auth import AuthHandler


if TYPE_CHECKING:
    from app.models import Users

auth_handler = AuthHandler()

Auth = Annotated["Users", Depends(auth_handler.auth_wrapper)]

auth = Depends(auth_handler.auth_wrapper)
