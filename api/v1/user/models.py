from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint

from core.db.base import Base


user_roles_table = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id")),
    PrimaryKeyConstraint('user_id', 'role_id'),
)


class UserModel(Base):
    def __init__(self):
        pass

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    roles: List[RoleModel] = relationship(
        "RoleModel",
        secondary=user_roles_table,
        back_populates="users",
    )

class RoleModel(Base):
    def __init__(self):
        pass

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(10), default="user")

    users = relationship(
        "UserModel", secondary=user_roles_table, back_populates="roles"
    )

class RefreshTokenModel(Base):
    def __init__(self):
        pass

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=False) #hash

    users = relationship(
        "UserModel", secondary=user_roles_table, back_populates="roles"
    )

    roles: List[RoleModel] = relationship(
        "RoleModel",
        secondary=user_roles_table,
        back_populates="users",
    )