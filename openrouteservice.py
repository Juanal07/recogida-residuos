import requests
import json

#body = {"coordinates":[[-3.897235,40.518348],[-3.900518,40.519669]]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248d78346ffbd314936809ae8a93c99522a',
    'Content-Type': 'application/json; charset=utf-8'
}

def get_distance(lon1, lat1, lon2, lat2):
    nav_request =  {"coordinates":[[lon1,lat1],[lon2,lat2]]}
    endpoint = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=nav_request, headers=headers)
    response = endpoint.json()
    dist = 0
    if endpoint.status_code == 200:
        dist = response["routes"][0]["summary"]["distance"]

    return dist
print(get_distance(-3.897235,403.518348,-3.900518,40.519669))