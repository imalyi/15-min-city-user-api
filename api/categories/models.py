from api.database import (
    Base,
    str_256,
    pk_int,
    required_int,
    required_string,
)
from typing import Annotated, List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Index, UniqueConstraint


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[pk_int]
    title: Mapped[str_256]
    collection_id: Mapped[int] = mapped_column(
        ForeignKey("category_collections.id")
    )

    order: Mapped[required_int]
    is_default: Mapped[bool] = mapped_column(default=False)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    minimum_subscription_level: Mapped[required_int] = 0

    __table_args__ = (UniqueConstraint("title", "collection_id"),)
