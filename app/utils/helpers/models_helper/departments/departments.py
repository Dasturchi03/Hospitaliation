from typing import Protocol, Awaitable, List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.doctors import Doctor
    from app.models.day_quota import DayQuota
    from app.models.appointments import Appointment


class DepartmentAwaitableAttrs(Protocol):
    
    @property
    def doctors(self) -> Awaitable[List["Doctor"]]: ...

    @property
    def day_quotas(self) -> Awaitable[List["DayQuota"]]: ...

    @property
    def appointments(self) -> Awaitable[List["Appointment"]]: ...
