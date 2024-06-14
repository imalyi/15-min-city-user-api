from pydantic import ValidationError
from typing import List
from .mongo_database import MongoDatabase 
from .model import Category
import geojson
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
            coords.append([document.get('location')[0], document.get('location')[1]])
        
        points = np.array(coords)
        hull = ConvexHull(points)
        hull_points = points[hull.vertices].tolist()
        hull_points.append(hull_points[0])
        polygon = geojson.Feature(geometry=geojson.Polygon([hull_points]), properties={"name": "Sample Polygon"})
        feature_collection = geojson.FeatureCollection([polygon])
        geojson_dict = geojson.loads(geojson.dumps(feature_collection))


        return geojson_dict




 
h = HeatMapModel()
h.generate([Category(main_category='Transport', category='Rowery MEVO')])