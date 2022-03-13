import random
import string
import json
import pandas as pd
import requests
import json
import numpy as np


# convert json file to df
f = open("drivers.json")
json_drivers = json.load(f)
df_drivers = pd.DataFrame.from_dict(json_drivers)
print(df_drivers)

f = open("locations.json")
json_locations = json.load(f)
df_locations = pd.DataFrame.from_dict(json_locations)
print(df_locations)

def get_distance(lon1, lat1, lon2, lat2):
    endpoint = "http://router.project-osrm.org/route/v1/driving/"

    nav_request = "{},{};{},{}?overview=false".format(lon1, lat1, lon2, lat2)
    request = endpoint + nav_request
    response = json.loads(requests.get(request).text)
    print(request)

    dist = 0
    if len(response["routes"]) > 0:

        dist = response["routes"][0]["distance"]

    return dist

print(get_distance("13.397634","52.529407","13.428555","52.523219"))

def create_distance_matrix(latList, lonList):

    n = len(latList)

    M = np.zeros(shape=(n, n))

    for i in range(n):
        for j in range(i + 1, n):

            dist = get_distance(latList[i], lonList[i], latList[j], lonList[j])

            M[i, j] = dist
            M[j, i] = dist

    return M


def create_model(df_drivers, df_locations):

    ## multidepot

    n_drivers = df_drivers.shape[0]

    lng_combined = df_drivers.lng.to_list() + df_locations.lng.to_list()
    lat_combined = df_drivers.lat.to_list() + df_locations.lat.to_list()

    data = {}
    data["latitudes"] = [float(lat) for lat in lat_combined]
    data["longitudes"] = [float(lng) for lng in lng_combined]
    data["distance_matrix"] = create_distance_matrix(lat_combined, lng_combined)
    data["demands"] = [0] * n_drivers + df_locations.demand.to_list()
    data["vehicle_capacities"] = df_drivers.capacity.to_list()
    data["num_vehicles"] = n_drivers
    data["depot"] = 0

    data["starts"] = []
    data["ends"] = []
    for i in range(n_drivers):
        data["starts"].append(i)
        data["ends"].append(i)

    return data


# data = create_model(df_drivers, df_locations)
# print(data)
