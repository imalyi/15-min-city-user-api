from api.database import Base, required_int, required_string
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey


class InviteCode(Base):
    __tablename__ = "invite_codes"
    id: Mapped[required_int] = mapped_column(primary_key=True)
    level: Mapped[required_int]
    days: Mapped[required_int]
    code: Mapped[required_string]
    description: Mapped[required_string]
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    activated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    __table_args__ = (UniqueConstraint("code"),)
