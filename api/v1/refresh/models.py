from core.db.base import Base

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint, Boolean, DateTime


def default_exp():
    return datetime.now(timezone.utc) + timedelta(seconds=settings.EXPIRE_AT_REFRESH)


class RefreshTokenModel(Base):
    __tablename__ = 'refresh_tokens'


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False) #Хэш токена
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    exp_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_exp)