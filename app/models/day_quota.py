from typing import TYPE_CHECKING, cast
from datetime import datetime, date
from sqlalchemy import Integer, Date, DateTime, ForeignKey, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.utils.helpers.models_helper.day_quota import DayQuotaAwaitableAttrs


if TYPE_CHECKING:
    from app.models.departments import Department


class DayQuota(Base):
    __tablename__ = "day_quotas"
    __table_args__ = (
        UniqueConstraint("department_id", "date", name="uq_dayquota_department_date"),
        Index("ix_dayquota_department_date", "department_id", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    date: Mapped["date"] = mapped_column(Date)

    base_slots: Mapped[int] = mapped_column(Integer, default=0)
    extra_slots: Mapped[int] = mapped_column(Integer, default=0)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    department: Mapped["Department"] = relationship(back_populates="day_quotas")

    def total_slots(self) -> int:
        return (self.base_slots or 0) + (self.extra_slots or 0)

    def __repr__(self) -> str:
        return f"<DayQuota dept={self.department_id} date={self.date} total={self.total_slots()}>"

    @property
    def awaitable_attrs(self) -> DayQuotaAwaitableAttrs:
        return cast(DayQuotaAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
