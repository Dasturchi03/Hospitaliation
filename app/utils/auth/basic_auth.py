from fastapi import Security, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from app.models.users import Users
from app.db.base import session_manager


class BasicAuthHandler:
    security = HTTPBasic()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def auth_wrapper(self, credentials: HTTPBasicCredentials = Security(security)):
        with session_manager() as db_session:
            user: Users = db_session.query(Users).filter(Users.username == credentials.username).first()
        if not user:
            raise HTTPException(status_code=403, detail='Not authenticated!')

        if not self.verify_password(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password!")

        return True
