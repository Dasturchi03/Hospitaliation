from typing import List, TYPE_CHECKING, cast
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.api.rbac.models.associations import role_permissions
from app.utils.helpers.models_helper.rbac import RolesAwaitableAttrs


if TYPE_CHECKING:
    from app.api.rbac.models import Permissions


class Roles(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    level: Mapped[int] = mapped_column()

    permissions: Mapped[List["Permissions"]] = relationship(
        "Permissions",
        back_populates='roles',
        secondary=role_permissions,
        lazy='subquery'
    )

    @property
    def awaitable_attrs(self) -> RolesAwaitableAttrs:
        return cast(RolesAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
