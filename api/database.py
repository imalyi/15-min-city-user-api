import databases
import sqlalchemy
from api.config import config

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(config.DATABASE_URL)


category_table = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("parent_category", sqlalchemy.String),
    sqlalchemy.Column("child_category", sqlalchemy.String),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.UniqueConstraint(
        "parent_category", "child_category", name="unique_parent_child"
    ),
)


address_table = sqlalchemy.Table(
    "addresses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("street", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("city", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postcode", sqlalchemy.String, nullable=True),
    sqlalchemy.UniqueConstraint("street", "city", "postcode"),
    sqlalchemy.Column("lat", sqlalchemy.Float),
    sqlalchemy.Column("lng", sqlalchemy.Float),
)


poi_table = sqlalchemy.Table(
    "pois",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "address_id", sqlalchemy.ForeignKey("addresses.id"), nullable=False
    ),
    sqlalchemy.UniqueConstraint("name", "address_id"),
)


poi_category_table = sqlalchemy.Table(
    "pois_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("poi_id", sqlalchemy.ForeignKey("pois.id"), nullable=False),
    sqlalchemy.Column(
        "category_id", sqlalchemy.ForeignKey("categories.id"), nullable=False
    ),
    sqlalchemy.UniqueConstraint("poi_id", "category_id"),
)

poi_address_table = sqlalchemy.Table(
    "poi_addresses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("poi_id", sqlalchemy.ForeignKey("pois.id"), nullable=False),
    sqlalchemy.Column(
        "address_id", sqlalchemy.ForeignKey("addresses.id"), nullable=False
    ),
    sqlalchemy.UniqueConstraint("poi_id", "address_id"),
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
