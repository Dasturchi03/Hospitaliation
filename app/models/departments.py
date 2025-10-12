from typing import List, TYPE_CHECKING, cast
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.utils.helpers.models_helper.departments import DepartmentAwaitableAttrs


if TYPE_CHECKING:
    from app.models.doctors import Doctor
    from app.models.day_quota import DayQuota
    from app.models.appointments import Appointment


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    default_quota: Mapped[int] = mapped_column(server_default='5')
    is_active: Mapped[bool] = mapped_column(default=True)

    doctors: Mapped[List["Doctor"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    day_quotas: Mapped[List["DayQuota"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    appointments: Mapped[List["Appointment"]] = relationship(
        back_populates="department"
    )

    def __repr__(self) -> str:
        return f"<Department id={self.id} name={self.name!r}>"

    @property
    def awaitable_attrs(self) -> DepartmentAwaitableAttrs:
        return cast(DepartmentAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
