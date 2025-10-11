from typing import Protocol, List, TYPE_CHECKING, Awaitable


if TYPE_CHECKING:
    from app.api.rbac.models import Permissions


class RolesAwaitableAttrs(Protocol):
    
    @property
    def permissions(self) -> Awaitable[List["Permissions"]]: ...
