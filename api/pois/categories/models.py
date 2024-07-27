from api.database import (
    Base,
    pk_int,
    required_int,
    required_string,
)
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String


class POICategories(Base):
    __tablename__ = "pois_categories"
    id: Mapped[pk_int]
    poi_id: Mapped[required_int] = mapped_column(
        ForeignKey("pois.id", ondelete="CASCADE")
    )
    category_id: Mapped[required_int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), nullable=True
    )

    __table_args__ = (UniqueConstraint("poi_id", "category_id"),)
