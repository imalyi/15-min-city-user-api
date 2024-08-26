from api.database import (
    Base,
    str_256,
    pk_int,
    required_int,
    required_string,
)
from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Index, UniqueConstraint, Computed
import geoalchemy2
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "ticket"
    id: Mapped[pk_int]
    user_id: Mapped[required_int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), server_default=func.now(), nullable=True
    )

    __table_args__ = (UniqueConstraint("user_id", "message"),)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
            "id": self.id,
        }
