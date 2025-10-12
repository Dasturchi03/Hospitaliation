from typing import List, cast, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.db.base import Base
from app.api.auth.models.associations import user_role
from app.utils.helpers.models_helper.users import UserAwaitableAttrs


if TYPE_CHECKING:
    from app.models import *


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'Пользователи'}
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), comment="Имя пользователя")
    password: Mapped[str] = mapped_column(String(255), comment="Пароль")

    roles: Mapped[List['Roles']] = relationship(
        backref='users',
        secondary=user_role
    )
    doctors: Mapped[List["Doctor"]] = relationship(
        back_populates='user'
    )

    def __str__(self):
        return f'{self.id}. {self.username}'

    @property
    def awaitable_attrs(self) -> UserAwaitableAttrs:
        return cast(UserAwaitableAttrs, AsyncAttrs._AsyncAttrGetitem(self))
