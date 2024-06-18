from database.googlemaps_distance_calculator import GoogleMapsDistanceCalculator

def fetch_route_time(report):
    gmaps = GoogleMapsDistanceCalculator(from_=report.address)
    data = {'custom_addresses': {}}
    for address in report.requested_addresses:
        if not address in data['custom_addresses']:
            data['custom_addresses'][address] = {}
        data['custom_addresses'][address]['commute_time'] = gmaps.calc(to=address)
    return data