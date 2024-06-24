from .models import ResidentialBuilding
from .models import Category
import os
import logging
import re


MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", '15min')
MONGO_CONNECT = os.environ.get("MONGO_CONNECT", "mongodb://root:example@node:27777/")

logger = logging.getLogger(f"{__name__}_Database")

class MongoDatabase:
    def __init__(self):
        self.db_name = MONGO_DB_NAME

    def search_by_partial_name(self, address: str):
        try:
            regex = re.compile(f'.*{re.escape(address)}.*', re.IGNORECASE)
            result = ResidentialBuilding.objects(address__street=regex).limit(5)
            return [doc.address.street for doc in result]
        except Exception as e:
            logger.error(f"Error executing MongoDB query: {e}")
            return []

    def get_categories(self):
        result = Category.objects.all()
        return result
