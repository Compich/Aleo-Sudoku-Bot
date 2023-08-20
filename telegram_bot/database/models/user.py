import datetime as dt
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

import enums
from database.base import Base, func, int64, str_40, str_100, str_53, str_59

if TYPE_CHECKING:
    from database.models.game import Game


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int64] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[Optional[str_40]]
    reg_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    address: Mapped[Optional[str_100]]
    view_key: Mapped[Optional[str_53]]
    private_key: Mapped[Optional[str_59]]
    address_privacy: Mapped[Optional[enums.AddressPrivacy]] = mapped_column(
        Enum(enums.AddressPrivacy, name='address_privacy'),
        default=enums.AddressPrivacy.PRIVATE
    )

    games: Mapped[Optional[List['Game']]] = relationship(
        'Game',
        back_populates='user',
        order_by='Game.start_time'
    )

    def __repr__(self):
        return str(self.username)
