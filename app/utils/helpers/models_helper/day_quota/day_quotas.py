from typing import Protocol, Awaitable, List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.departments import Department


class DayQuotaAwaitableAttrs(Protocol):
    
    @property
    def departments(self) -> Awaitable[List["Department"]]: ...
