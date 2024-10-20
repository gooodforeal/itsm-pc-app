from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base, int_pk


class Incidents(Base):
    __tablename__ = "incidents"

    id: Mapped[int_pk]
    status: Mapped[str]
    topic: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship(
        "Users",
        back_populates="incidents",
    )
