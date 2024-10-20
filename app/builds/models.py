from sqlalchemy import text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk


class Builds(Base):
    __tablename__ = "builds"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))

    user = relationship(
        "Users",
        back_populates="builds",
    )

    client = relationship(
        "Clients",
        back_populates="builds",
    )

    components_replied: Mapped[list["Components"]] = relationship(
        back_populates="builds_replied",
        secondary="builds_components",
    )


class BuildsComponents(Base):
    __tablename__ = "builds_components"

    build_id: Mapped[int] = mapped_column(
        ForeignKey("builds.id", ondelete="CASCADE"),
        primary_key=True,
    )
    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"),
        primary_key=True,
    )
