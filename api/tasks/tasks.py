from api.tasks.celery import celery
import openrouteservice as ors


def calc_distance(from_, to):
    client = ors.Client(key="", base_url="http://node:8080/ors")

    coordinates = [from_, to]
    response = client.directions(
        coordinates=coordinates,
        profile="foot-walking",
        format="json",
        validate=False,
    )
    return response.get("routes")[0].get("summary", {}).get("distance", -1)


# @celery.task
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

    print(nearest_pois)
