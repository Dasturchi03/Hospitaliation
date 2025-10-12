from typing import Protocol, Awaitable, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.departments import Department
    from app.models.doctors import Doctor


class AppointmentsAwaitableAttrs(Protocol):

    @property
    def department(self) -> Awaitable[Optional["Department"]]: ...

    @property
    def doctor(self) -> Awaitable[Optional["Doctor"]]: ...

    @property
    def created_by_user(self) -> Awaitable["Doctor"]: ...
