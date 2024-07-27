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

# TODO: добавить фильтрацию


class POI(Base):
    __tablename__ = "pois"
    id: Mapped[pk_int]
    name: Mapped[required_string]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), nullable=True
    )
    description: Mapped[str] = mapped_column(nullable=True)
    opening_hours: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)
    place_id_google_api: Mapped[str] = mapped_column(nullable=True)
    price_level: Mapped[str] = mapped_column(nullable=True)
    types: Mapped[list[str]] = mapped_column(ARRAY(String))
    address_id: Mapped[required_int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE")
    )
    __table_args__ = (UniqueConstraint("name", "place_id_google_api"),)
