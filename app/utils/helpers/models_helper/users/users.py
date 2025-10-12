from typing import Protocol, Awaitable, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.api.rbac.models import Roles
    from app.models.doctors import Doctor


class UserAwaitableAttrs(Protocol):

    @property
    def roles(self) -> Awaitable[List["Roles"]]: ...

    @property
    def doctors(self) -> Awaitable[List["Doctor"]]: ...
