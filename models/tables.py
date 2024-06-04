from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(start=10), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(Identity(start=10), primary_key=True)
    data: Mapped["Data"] = relationship(back_populates="level")

class Data(Base):
    __tablename__ = "datas"

    id: Mapped[int] = mapped_column(Identity(start=10), primary_key=True)
    size: Mapped[int] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column()
    start_x: Mapped[int] = mapped_column(nullable=False)
    start_y: Mapped[int] = mapped_column(nullable=False)
    end_x: Mapped[int] = mapped_column(nullable=False)
    end_y: Mapped[int] = mapped_column(nullable=False)
    lvl_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    level: Mapped["Level"] = relationship(back_populates="data")
