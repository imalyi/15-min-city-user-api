from api.category_collections.categories.models import Categories
from api.dao.base import BaseDAO


class CategoryDAO(BaseDAO):
    model = Categories
