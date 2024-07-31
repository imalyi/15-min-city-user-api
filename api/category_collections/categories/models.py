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
from datetime import datetime
from sqlalchemy import func


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    collection_id: Mapped[int] = mapped_column(
        ForeignKey("category_collections.id")
    )

    order: Mapped[int]
    is_default: Mapped[bool] = mapped_column(default=False)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    minimum_subscription_level: Mapped[required_int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (UniqueConstraint("title", "collection_id"),)