import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select
from app.api.auth.models.users import Users
from app.core.security import security as app_security
from app.utils.di.db_ctx import DB


class AuthHandler():

    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = app_security.AUTH_SECRET_KEY

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def encode_token(cls, username: str):
        payload = {
            'iat': datetime.now(tz=timezone.utc),
            'exp': datetime.now(tz=timezone.utc) + timedelta(days=3),
            'username': username
        }
        return jwt.encode(
            payload,
            cls.secret,
            algorithm='HS256'
        )

    async def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if 'username' not in payload:
                raise HTTPException(status_code=403, detail={'status':'Signature has expired'})
            stmt = select(
                Users
            ).where(
                Users.username == payload['username']
            )
            resp = (await DB.execute(stmt)).unique()
            user = resp.scalar_one_or_none()
            if (user is None):
                raise HTTPException(status_code=403, detail='Not authenticated!')
            return user

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail={'status':'Signature has expired'})
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail={'status':'Invalid token'})

    async def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return await self.decode_token(auth.credentials)
