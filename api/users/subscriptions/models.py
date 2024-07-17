from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import date


class UserSubscription(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    subscription_level: Mapped[int] = mapped_column(
        ForeignKey("subscription_levels.level", ondelete="CASCADE")
    )
    date_from: Mapped[date]
    date_to: Mapped[date]
