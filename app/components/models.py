from sqlalchemy.orm import Mapped, relationship
from app.database import Base, int_pk


class Components(Base):
    __tablename__ = "components"

    id: Mapped[int_pk]
    name: Mapped[str]
    type: Mapped[str]
    price: Mapped[float]

    builds_replied: Mapped[list["Builds"]] = relationship(
        back_populates="components_replied",
        secondary="builds_components",
    )
