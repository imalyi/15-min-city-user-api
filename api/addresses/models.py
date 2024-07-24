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


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[pk_int]
    street_type: Mapped[str] = mapped_column(nullable=True)
    street_name: Mapped[required_string]
    house_number: Mapped[required_string]
    city: Mapped[required_string]
    postcode: Mapped[str] = mapped_column(nullable=True)
    geometry: Mapped[str] = mapped_column(geoalchemy2.Geometry("MULTIPOLYGON"))
    full_address: Mapped[str] = mapped_column(
        String,
        Computed(
            "COALESCE(street_type || ' ', '') || street_name || ' ' || house_number || ', ' || city || COALESCE(', ' || postcode, '')"
        ),
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            "street_type",
            "street_name",
            "house_number",
            "city",
        ),
    )
