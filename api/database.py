import databases
import sqlalchemy
from api.config import config
import geoalchemy2

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(config.DATABASE_URL)


category_collections_table = sqlalchemy.Table(
    "category_collections",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.UniqueConstraint("title"),
)


category_table = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column(
        "collection_id", sqlalchemy.ForeignKey("category_collections.id")
    ),
    sqlalchemy.Column("order", sqlalchemy.Integer),
    sqlalchemy.Column("is_default", sqlalchemy.Boolean),
    sqlalchemy.Column("is_hidden", sqlalchemy.Boolean),
    sqlalchemy.Column("minimum_subscription_level", sqlalchemy.Integer),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.UniqueConstraint("title", "collection_id"),
)


address_table = sqlalchemy.Table(
    "addresses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("street", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("city", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postcode", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "geometry", geoalchemy2.Geometry("MULTIPOLYGON"), nullable=False
    ),
    sqlalchemy.UniqueConstraint("street", "city", "postcode"),
)


poi_table = sqlalchemy.Table(
    "pois",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.UniqueConstraint("name"),
)


poi_category_table = sqlalchemy.Table(
    "pois_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "poi_id", sqlalchemy.ForeignKey("pois.id"), nullable=False
    ),
    sqlalchemy.Column(
        "category_id", sqlalchemy.ForeignKey("categories.id"), nullable=False
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "last_seen_at",
        sqlalchemy.DateTime(timezone=True),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.UniqueConstraint("poi_id", "category_id"),
)

poi_address_table = sqlalchemy.Table(
    "poi_addresses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "poi_id", sqlalchemy.ForeignKey("pois.id"), nullable=False
    ),
    sqlalchemy.Column(
        "address_id", sqlalchemy.ForeignKey("addresses.id"), nullable=False
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "last_seen_at",
        sqlalchemy.DateTime(timezone=True),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.UniqueConstraint("poi_id", "address_id"),
)

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
    sqlalchemy.Column("level", sqlalchemy.Integer, default=0),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_activated", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column(
        "registration_date",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column("allow_telemetry", sqlalchemy.Boolean, default=True),
    sqlalchemy.UniqueConstraint("email"),
)

history_preference_table = sqlalchemy.Table(
    "history_preference",
    metadata,
    sqlalchemy.Column("id", primary_key=True),
    sqlalchemy.Column(
        "history_id", sqlalchemy.ForeignKey("history.id"), nullable=False
    ),
    sqlalchemy.Column("category_id", sqlalchemy.ForeignKey("categories.id")),
    sqlalchemy.UniqueConstraint("history_id", "category_id"),
)

history_custom_address_table = sqlalchemy.Table(
    "history_custom_address",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "custom_address_id",
        sqlalchemy.ForeignKey("addresses.id"),
        nullable=False,
    ),
)

history_table = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", primary_key=True),
    sqlalchemy.Column(
        "address_id", sqlalchemy.ForeignKey("addresses.id"), nullable=False
    ),
    sqlalchemy.Column(
        "user_id", sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
    sqlalchemy.Column(
        "datetime",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)


metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
