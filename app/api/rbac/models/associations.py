from sqlalchemy import Table, Column, ForeignKey
from app.db.base import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column('permission_id', ForeignKey("permissions.id")),
    Column('role_id', ForeignKey("roles.id"))
)
