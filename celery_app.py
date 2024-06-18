from celery import Celery
import os
from typing import List
from database.model import Category
from database.mongo_database import MongoDatabase
import geojson
import json
import redis

redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_CACHE', "redis://192.168.0.105:5123/5"), decode_responses=True)

celery_app = Celery(
    'heatmap_worker',
    broker=os.environ.get("CELERY_BROKER_URL", "redis://node:5123/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://node:5123/0")
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)


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


def generate_cache_key(categories: List[dict]) -> str:
    # Sort the categories list based on the name and value
    sorted_categories = sorted(categories, key=lambda x: (x['name'], x['value']))
    # Convert the sorted list to a JSON string to use as the cache key
    return json.dumps(sorted_categories)


@celery_app.task(bind=True)
def generate_heatmap_task(self, categories):
    try:
        h = HeatMapModel()
        result = h.generate(categories)
        # Generate cache key from sorted categories
        cache_key = generate_cache_key(categories)
        # Store the result in Redis with an expiration time (e.g., 1 hour)
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}