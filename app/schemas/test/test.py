from typing import List
from app.schemas.common import BaseSchema


class AddUser(BaseSchema):
    username: str
    password: str


class UserModel(AddUser):
    id: int


ListUsers = List[UserModel]
