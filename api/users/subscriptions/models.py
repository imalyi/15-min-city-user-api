from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import date, datetime


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    subscription_level: Mapped[int] = mapped_column(
        ForeignKey("subscription_levels.level", ondelete="CASCADE")
    )
    date_from: Mapped[date]
    date_to: Mapped[date]

    __table_args__ = (UniqueConstraint("user_id", "date_to", "date_from"),)

    @property
    def is_active(self):
        if self.date_to >= date.today():
            return True
        return False
