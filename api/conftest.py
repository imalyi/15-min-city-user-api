from api.config import config

config.DATABASE_URL = (
    "postgresql+asyncpg://myuser:mysecretpassword@node:5432/mydatabase"
)
