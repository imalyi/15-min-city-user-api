from typing import Annotated

import sqlalchemy
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker

from api.config import config

print(
    config.DATABASE_URL,
    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!_______________________-",
)
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
