from typing import Literal, Optional, Any
from .base import BaseSchema


class Result(BaseSchema):
    result: Literal["Ok", "Failed"]
    message: Optional[str] = None
    data: Optional[Any] = None
