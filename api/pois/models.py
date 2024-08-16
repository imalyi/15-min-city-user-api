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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from api.pois.categories.models import poi_category_association_table
from typing import List


class POI(Base):
    __tablename__ = "pois"
    id: Mapped[pk_int]
    name: Mapped[required_string]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), nullable=True
    )

    address_id: Mapped[int] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False
    )
    address: Mapped["Address"] = relationship(
        back_populates="pois", uselist=False, lazy="joined"
    )
    categories: Mapped[List["Categories"]] = relationship(
        back_populates="pois",
        secondary=poi_category_association_table,
        lazy="joined",
    )
    __table_args__ = (UniqueConstraint("name", "address_id"),)
