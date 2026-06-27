from sqlalchemy.dialects.sqlite import INTEGER, TEXT, JSON
from sqlalchemy.orm import mapped_column, Mapped

from .core.base import Base


class OutBox(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    queue_name: Mapped[str] = mapped_column(TEXT, nullable=False)
    message: Mapped[dict] = mapped_column(JSON, nullable=False)