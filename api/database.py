from typing import Annotated

import sqlalchemy
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker

from api.config import config

str_256 = Annotated[str, 256]

pk_int = Annotated[int, mapped_column(primary_key=True)]
required_int = Annotated[int, mapped_column(nullable=False)]
required_string = Annotated[str, mapped_column(nullable=False)]

engine = create_async_engine(config.DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    config.DATABASE_URL, echo=False, pool_size=15
)

"""
subscription_level_table = sqlalchemy.Table(
    "subscription_levels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("requests_per_day", sqlalchemy.Integer, default=3),
    sqlalchemy.Column(
        "custom_address_check", sqlalchemy.Boolean, default=False
    ),
    sqlalchemy.Column(
        "heatmap_generation_permission", sqlalchemy.Boolean, default=False
    ),
    sqlalchemy.Column("level", sqlalchemy.Integer, default=0, nullable=False),
    sqlalchemy.UniqueConstraint("level"),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
)

user_subscriptions = sqlalchemy.Table(
    "user_subscriptions",
    metadata,
    sqlalchemy.Column(
        "user_id", sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
    sqlalchemy.Column(
        "subscription_id", sqlalchemy.ForeignKey("subscription_levels.id")
    ),
    sqlalchemy.Column("date_from", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("date_to", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.UniqueConstraint("user_id", "date_from"),
    sqlalchemy.UniqueConstraint("user_id", "date_to"),
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)


# запрос на вставку statement, на выборку query
# переделать на декалативный вид
"""
