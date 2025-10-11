from typing import Protocol, List, Awaitable, TYPE_CHECKING


if TYPE_CHECKING:
    from app.api.rbac.models import Permissions


class PermissionCategoryAwaitableAttrs(Protocol):

    @property
    def endpoints(self) -> Awaitable[List["Permissions"]]: ...
