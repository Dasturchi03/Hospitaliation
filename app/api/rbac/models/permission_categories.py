from typing import List, cast, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.utils.helpers.models_helper.rbac import PermissionCategoryAwaitableAttrs


if TYPE_CHECKING:
    from app.api.rbac.models import Permissions


class PermissionCategory(Base):
    __tablename__ = 'permission_category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    endpoints: Mapped[List["Permissions"]] = relationship(
        "Permissions",
        back_populates="category"
    )

    @property
    def awaitable_attrs(self) -> PermissionCategoryAwaitableAttrs:
        return cast(PermissionCategoryAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
