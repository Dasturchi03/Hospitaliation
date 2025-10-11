from fastapi.exceptions import HTTPException
from app.api.auth.schemas import user_auth as sc
from app.services.users import users
from app.utils.deps.auth import AuthHandler


async def login_user(request: sc.UserLoginRequest):
    user = await users.get_user(username=request.username)
    await user.awaitable_attrs.roles

    if AuthHandler.verify_password(request.password, user.password):
        token = AuthHandler.encode_token(username=user.username)
        permissions = set()

        for role in user.roles:
            await role.awaitable_attrs.permissions
            permissions.update(role.permissions)

        return sc.UserLoggedIn(
            token=token,
            user=user,
            permissions=permissions
        )

    raise HTTPException(401, "Parol noto'g'ri")
