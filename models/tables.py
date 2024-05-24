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
    size: Mapped[int] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column()
