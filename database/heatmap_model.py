from pydantic import ValidationError
from typing import List
from .mongo_database import MongoDatabase 
from .model import Category
import geojson


def ensure_closed_ring(ring):
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        return ring

class HeatMapModel:
    def __init__(self):
        self._db = MongoDatabase().db

    def generate(self, required_categories: List[Category]):
        conditions = {}
        for c in required_categories:
            conditions[f"points_of_interest.{c.main_category}.{c.category}"] = { "$ne": []}
        results = self._db['address'].find(conditions)
        features = []
        i = 0
        for doc in results:
                geometry = {
                "type": "Polygon",
                "coordinates": [ensure_closed_ring((ring)) for ring in doc['geometry']]
            }
                feature = geojson.Feature(
                    geometry=geometry,
                    
                )
                features.append(feature)
                if i % 1000 == 0:
                    print(f"Handled {i} docs")
                i += 1
        feature_collection = geojson.FeatureCollection(features)
        feature_collection_geojson_str = geojson.dumps(feature_collection)
        feature_collection_dict = geojson.loads(feature_collection_geojson_str)
        return feature_collection_dict