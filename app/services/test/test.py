from sqlalchemy import select
from app.models import Users
from app.services.common import _get_all, _get_one
from app.schemas.test import test as sc
from app.utils.di.db_ctx import DB
from app.utils.auth.auth import AuthHandler
from app.utils.exc import DataBaseError


async def test(request: sc.AddUser):
    stmt = select(
        Users
    ).where(
        Users.username == request.username
    )
    user_ = await _get_one(stmt)

    if user_:
        raise DataBaseError("User already exists!")

    user = Users(
        username = request.username,
        password = AuthHandler.get_password_hash(request.password)
    )

    print(user)

    DB.add(user)
    await DB.flush()
    await DB.refresh(user)

    return sc.UserModel.model_validate(user)


async def get_users():
    stmt = select(Users)

    return await _get_all(stmt)
