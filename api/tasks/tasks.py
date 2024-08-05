import openrouteservice as ors
from celery import shared_task
from geojson import Feature, FeatureCollection, Point

from api.config import config


def calc_distance(from_, to):
    client = ors.Client(key="", base_url=config.ORS_URL)

    coordinates = [from_, to]
    response = client.directions(
        coordinates=coordinates,
        profile="foot-walking",
        format="json",
        validate=False,
    )
    return response.get("routes")[0].get("summary", {}).get("distance", -1)


def generate_geojson(nearest_points_dict):
    features = []

    # Add start_point as a GeoJSON feature
    if "start_point" in nearest_points_dict:
        start_point = nearest_points_dict["start_point"]["location"]
        point = Point((start_point["lon"], start_point["lat"]))
        features.append(
            Feature(geometry=point, properties={"name": "Start Point"})
        )

    # Add POIs as GeoJSON features
    if "pois" in nearest_points_dict:
        for collection_title, categories in nearest_points_dict[
            "pois"
        ].items():
            for category_title, pois in categories.items():
                for poi in pois:
                    point = Point(
                        (poi["location"]["lon"], poi["location"]["lat"])
                    )
                    properties = {
                        "name": poi["name"],
                        "address": poi["address"],
                        "category": category_title,
                        "collection": collection_title,
                        "distance": poi["distance"],
                    }
                    features.append(
                        Feature(geometry=point, properties=properties)
                    )

    # Create GeoJSON FeatureCollection
    geojson_obj = FeatureCollection(features)
    return geojson_obj


@shared_task
def generate_report(nearest_pois: dict):
    from_ = [
        nearest_pois.get("start_point", {}).get("lon"),
        nearest_pois.get("start_point", {}).get("lat"),
    ]
    for collection, categories in nearest_pois["pois"].items():
        for category, pois in categories.items():
            i = 0
            for poi in pois:
                to = [
                    poi.get("location", {}).get("lon"),
                    poi.get("location", {}).get("lat"),
                ]
                distance = calc_distance(from_, to)
                nearest_pois["pois"][collection][category][i][
                    "distance"
                ] = distance
                i += 1

    return {"full": nearest_pois, "geojson": generate_geojson(nearest_pois)}
