from sqlalchemy.orm import Mapped, relationship
from app.database import Base, int_pk


class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[int_pk]
    fio: Mapped[str]

    builds = relationship(
        "Builds",
        back_populates="client",
    )
