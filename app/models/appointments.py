from typing import TYPE_CHECKING, cast
from datetime import datetime, date as PyDate
from sqlalchemy import Integer, String, Text, Date, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.utils.helpers.models_helper.appointments import AppointmentsAwaitableAttrs


if TYPE_CHECKING:
    from app.models.departments import Department
    from app.models.doctors import Doctor


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        Index("ix_appointment_department_date_slot", "department_id", "date", "slot_no"),
        Index("ix_appointment_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="RESTRICT"), index=True)
    date: Mapped[PyDate] = mapped_column(Date, index=True)

    slot_no: Mapped[int] = mapped_column(Integer)

    doctor_id: Mapped[int | None] = mapped_column(ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)

    patient_fullname: Mapped[str] = mapped_column(String(200))
    birth_date: Mapped[PyDate | None] = mapped_column(Date, nullable=True)
    age_text: Mapped[str | None] = mapped_column(String(60))
    diagnosis: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    purpose: Mapped[str | None] = mapped_column(String(255))
    doctor_name_text: Mapped[str | None] = mapped_column(String(200))

    note_for_head: Mapped[str | None] = mapped_column(Text)
    note_public: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(20), default='planned')

    created_by: Mapped[int | None] = mapped_column(ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    department: Mapped["Department"] = relationship(back_populates="appointments")
    doctor: Mapped["Doctor | None"] = relationship(back_populates="appointments", foreign_keys=[doctor_id])
    created_by_user: Mapped["Doctor"] = relationship(back_populates="created_appointments", foreign_keys=[created_by])

    def __repr__(self) -> str:
        return f"<Appointment id={self.id} dept={self.department_id} {self.date} slot={self.slot_no} status={self.status}>"

    @property
    def awaitable_attrs(self) -> AppointmentsAwaitableAttrs:
        return cast(AppointmentsAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
