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

from typing import List


class CategoryCollections(Base):
    __tablename__ = "category_collections"
    id: Mapped[pk_int]
    title: Mapped[required_string]

    categories: Mapped[List["Categories"]] = relationship(
        backref="category_collections"
    )
    __table_args__ = (UniqueConstraint("title"),)
