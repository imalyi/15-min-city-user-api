from pydantic import ValidationError
from typing import List
from .mongo_database import MongoDatabase 
from .model import Category

from scipy.spatial import ConvexHull
import numpy as np


class HeatMapModel:
    def __init__(self):
        self._db = MongoDatabase().db

    def generate(self, requeired_categories: list[Category]):
        required_fields = []
        for c in requeired_categories:
            required_fields.append(f"{c.main_category}.{c.category}")

        conditions = {
            'points_of_interest.Zdrowie.Apteki': {"$exists": True, "$ne": []}
        }

        results = self._db['address'].find(conditions)

        coords = []
        for document in results:
            coords.append(document.get('location'))
        points = np.array(coords)
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        return hull_points.tolist()




 
#h = HeatMapModel()
#h.generate([Category(main_category='Transport', category='Rowery MEVO')])