from api.database import (
    Base,
    required_int,
    required_string,
)
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UniqueConstraint


class SubscriptionLevel(Base):
    __tablename__ = "subscription_levels"
    title: Mapped[required_string]

    report_requests_per_day: Mapped[required_int] = mapped_column(default=5)
    heatmap_requests_per_day: Mapped[required_int] = mapped_column(default=1)
    custom_address_check_per_day: Mapped[int] = mapped_column(default=5)

    report_generation_permission: Mapped[bool] = mapped_column(default=True)
    heatmap_generation_permission: Mapped[bool] = mapped_column(default=False)
    custom_address_check_permission: Mapped[bool] = mapped_column(default=True)
    level: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    __table_args__ = (UniqueConstraint("level"), UniqueConstraint("title"))
