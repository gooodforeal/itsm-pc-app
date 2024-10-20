from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    fio: Mapped[str]
    username: Mapped[str_uniq]
    password: Mapped[str]

    builds = relationship(
        "Builds",
        back_populates="user",
    )

    incidents = relationship(
        "Incidents",
        back_populates="user",
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
