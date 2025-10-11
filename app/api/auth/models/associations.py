from sqlalchemy import Table, Column, ForeignKey
from app.db.base import Base


user_role = Table(
    "user_role",
    Base.metadata,
    Column('user_id', ForeignKey("users.id")),
    Column('role_id', ForeignKey("roles.id"))
)
