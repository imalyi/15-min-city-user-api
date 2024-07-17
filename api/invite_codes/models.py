from api.database import Base, required_int, required_string
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint


class InviteCode(Base):
    __tablename__ = "invite_codes"
    id: Mapped[required_int] = mapped_column(primary_key=True)
    level: Mapped[required_int]
    days: Mapped[required_int]
    code: Mapped[required_string]

    __table_args__ = (UniqueConstraint("code"),)
