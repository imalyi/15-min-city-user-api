from celery import Celery
import os
from tasks import generate_heatmap_task


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

@celery_app.task(name="generate_heatmap_task")
def generate_heatmap_task(categories):
    #h = HeatMapModel()
    return 1*10000000#h.generate(categories)
