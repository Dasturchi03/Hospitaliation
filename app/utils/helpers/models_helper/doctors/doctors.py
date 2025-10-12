from typing import Protocol, Awaitable, List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.api.auth.models import Users
    from app.models.departments import Department
    from app.models.appointments import Appointment


class DoctorAwaitableAttrs(Protocol):
    
    @property
    def user(self) -> Awaitable[Optional["Users"]]: ...

    @property
    def department(self) -> Awaitable[Optional["Department"]]: ...

    @property
    def appointments(self) -> Awaitable[List["Appointment"]]: ...
