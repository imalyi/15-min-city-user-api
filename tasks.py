from celery_app import celery_app
from database.mongo_database import MongoDatabase
from database.model import Category
from typing import List
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
            conditions[f"points_of_interest.{c['main_category']}.{c['category']}"] = {"$ne": []}
        results = self._db['address'].find(conditions)
        features = []
        for i, doc in enumerate(results):
            geometry = {
                "type": "Polygon",
                "coordinates": [ensure_closed_ring(ring) for ring in doc['geometry']]
            }
            feature = geojson.Feature(geometry=geometry)
            features.append(feature)
            if i % 1000 == 0:
                print(f"Handled {i} docs")
        feature_collection = geojson.FeatureCollection(features)
        return geojson.loads(geojson.dumps(feature_collection))

@celery_app.task(name="generate_heatmap_task")
def generate_heatmap_task(categories):
    h = HeatMapModel()
    return h.generate(categories)
