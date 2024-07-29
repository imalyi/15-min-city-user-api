from api.database import (
    Base,
    str_256,
    pk_int,
    required_int,
    required_string,
)
from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from typing import List
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import String


class CategoryCollections(Base):
    __tablename__ = "category_collections"
    id: Mapped[pk_int]
    title: Mapped[required_string]
    order: Mapped[int]
    categories: Mapped[List["Categories"]] = relationship(
        backref="category_collections"
    )
    synonims: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    __table_args__ = (UniqueConstraint("title"),)
