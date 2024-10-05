from api.users.subscriptions.dao import UserSubscriptionDAO

from datetime import date, timedelta
from api.subscriptions.dao import SubscriptionDAO
from datetime import date


async def give_free_trial(user_id):
    trial_sub = await SubscriptionDAO.find_one_or_none(order_by=None, title = "after registration trial")
    data = {
        'user_id': user_id,
        'subscription_level': trial_sub.level,
        'date_from': date.today(),
        'date_to': date.today() + timedelta(days=1)
    }

    await UserSubscriptionDAO.insert_data(data)