from api.dao.base import BaseDAO
from api.subscriptions.models import SubscriptionLevel


class SubscriptionDAO(BaseDAO):
    model = SubscriptionLevel
