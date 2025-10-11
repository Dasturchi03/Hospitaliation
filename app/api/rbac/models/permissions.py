from typing import List, TYPE_CHECKING, cast
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.api.rbac.models.associations import role_permissions
from app.db.base import Base
from app.utils.helpers.models_helper.rbac import PermissionsAwaitableAttrs


if TYPE_CHECKING:
    from app.api.rbac.models import Roles, PermissionCategory


class Permissions(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    endpoint: Mapped[str] = mapped_column(String(255), unique=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('permission_category.id'), nullable=True)

    category: Mapped["PermissionCategory"] = relationship(
        "PermissionCategory",
        back_populates='endpoints'
    )
    roles: Mapped[List["Roles"]] = relationship(
        "Roles",
        back_populates='permissions',
        secondary=role_permissions
    )

    @property
    def awaitable_attrs(self) -> PermissionsAwaitableAttrs:
        return cast(PermissionsAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
