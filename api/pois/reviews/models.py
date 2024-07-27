from api.database import (
    Base,
    pk_int,
    required_int,
)
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import datetime
from sqlalchemy import func


class Review(Base):
    __tablename__ = "poi_reviews"
    id: Mapped[pk_int]
    poi_id: Mapped[required_int] = mapped_column(
        ForeignKey("pois.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), nullable=True
    )
    rating: Mapped[int] = mapped_column(nullable=True)
    wroted_at: Mapped[datetime]
    text: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (UniqueConstraint("text", "poi_id"),)
