from api.categories.models import Categories
from api.dao.base import BaseDAO


class CategoryDAO(BaseDAO):
    model = Categories
