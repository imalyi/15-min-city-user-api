from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Table,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from api.database import Base

# Define the association table with timestamps
poi_category_association_table = Table(
    "pois_categories",
    Base.metadata,
    Column(
        "poi_id",
        Integer,
        ForeignKey("pois.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("created_at", DateTime, server_default=func.now()),
    Column(
        "modified_at",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
    UniqueConstraint("poi_id", "category_id"),
)
