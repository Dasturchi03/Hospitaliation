from typing import TYPE_CHECKING, cast, List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.utils.helpers.models_helper.doctors import DoctorAwaitableAttrs


if TYPE_CHECKING:
    from app.api.auth.models import Users
    from app.models.departments import Department
    from app.models.appointments import Appointment


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=True)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="RESTRICT"), index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    speciality: Mapped[str | None] = mapped_column(String(120))

    user: Mapped["Users"] = relationship(back_populates="doctors", lazy="subquery")
    department: Mapped["Department"] = relationship(back_populates="doctors")
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="doctor", foreign_keys="Appointment.doctor_id")
    created_appointments: Mapped[List["Appointment"]] = relationship(back_populates='created_by_user', foreign_keys="Appointment.created_by")

    def __repr__(self) -> str:
        return f"<Doctor id={self.id} user_id={self.user_id} dept={self.department_id}>"

    @property
    def awaitable_attrs(self) -> DoctorAwaitableAttrs:
        return cast(DoctorAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
