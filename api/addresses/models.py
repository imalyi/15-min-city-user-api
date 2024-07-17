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


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[pk_int]
    street: Mapped[required_string]
    city: Mapped[required_string]
    postcode: Mapped[str] = mapped_column(nullable=True)
    geometry: Mapped[str] = mapped_column(geoalchemy2.Geometry("MULTIPOLYGON"))
    full_address: Mapped[str] = mapped_column(
        Computed("street || ', ' || city ||")
    )

    __table_args__ = (
        UniqueConstraint("street", "city", "postcode", "geometry"),
    )
