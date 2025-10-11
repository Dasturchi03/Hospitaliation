from typing import Protocol, Awaitable, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.api.rbac.models import Roles, PermissionCategory


class PermissionsAwaitableAttrs(Protocol):
    
    @property
    def roles(self) -> Awaitable[List["Roles"]]: ...

    @property
    def category(self) -> Awaitable["PermissionCategory"]: ...
