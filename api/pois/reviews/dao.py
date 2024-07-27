from api.dao.base import BaseDAO
from api.pois.reviews.models import Review


class ReviewDAO(BaseDAO):
    model = Review
