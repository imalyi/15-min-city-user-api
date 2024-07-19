from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime


class UserHistory(Base):
    __tablename__ = "history"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    request: Mapped[JSONB]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
