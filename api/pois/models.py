from api.database import (
    Base,
    pk_int,
    required_int,
    required_string,
)
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint


class POI(Base):
    __tablename__ = "pois"
    id: Mapped[pk_int]
    name: Mapped[required_string]
    __table_args__ = (UniqueConstraint("name"),)


class POICategories(Base):
    __tablename__ = "pois_categories"
    id: Mapped[pk_int]
    poi_id: Mapped[required_int] = mapped_column(
        ForeignKey("pois.id", ondelete="CASCADE")
    )
    category_id: Mapped[required_int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )

    __table_args__ = (UniqueConstraint("poi_id", "category_id"),)


class POIAddresses(Base):
    __tablename__ = "poi_addresses"
    id: Mapped[pk_int]
    poi_id: Mapped[required_int] = mapped_column(
        ForeignKey("pois.id", ondelete="CASCADE")
    )
    address_id: Mapped[required_int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE")
    )

    __table_args__ = (UniqueConstraint("address_id", "poi_id"),)
