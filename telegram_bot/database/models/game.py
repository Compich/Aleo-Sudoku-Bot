import datetime as dt
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

import enums
from database.base import Base, func, int64, str_81

if TYPE_CHECKING:
    from database.models.user import User


class Game(Base):
    __tablename__ = 'games'

    game_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int64] = mapped_column(
        ForeignKey('users.user_id')
    )
    difficulty: Mapped[enums.SudokuDifficulty] = mapped_column(
        Enum(enums.SudokuDifficulty, name='sudoku_difficulty')
    )
    board_str: Mapped[str_81]
    start_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    end_time: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    user: Mapped['User'] = relationship(back_populates='games')
