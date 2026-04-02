from core.db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint
from api.v1.user.models import user_roles_table, RoleModel


class RefreshTokenModel(Base):
    def __init__(self):
        pass

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=False) #hash

    users = relationship(
        "UserModel", secondary=user_roles_table, back_populates="roles"
    )

    roles: Mapped[RoleModel] = relationship(
        "RoleModel",
        secondary=user_roles_table,
        back_populates="users",
    )