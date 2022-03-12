import random
import string
import json
import pandas as pd
import requests
import json
import numpy as np


def load_data(file_dr, file_loc):
    def create_df(dic):
        c_names = [key for key in dic[0].keys()]
        df = pd.DataFrame(columns=c_names)
        i = 0
        for elem in dic:
            vals = []
            for c in c_names:
                vals.append(elem[c])
            df.loc[i] = vals
            i += 1
        return df

    f = open("drivers.json")
    json_drivers = json.load(f)
    f = open("locations.json")
    json_locations = json.load(f)
    df_drivers = create_df(json_drivers)
    df_locations = create_df(json_locations)
    # filtrar locations < 30
    # df_locations = df_locations[df_locations.demand > 30]
    return df_drivers, df_locations


df_drivers, df_locations = load_data("drivers.json", "locations.json")

print(df_drivers)
print(df_locations)


def reverse_geo(lat, lon):
    gmaps = googlemaps.Client(key=api_key)
    geocode = gmaps.reverse_geocode((lat, lon))

    loc = ""

    for x in geocode[0]["address_components"]:
        loc += x["long_name"] + " "

    return loc[:-1]


def get_route_points(lat1, lon1, lat2, lon2):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

    origin = reverse_geo(lat1, lon1).replace(" ", "+")
    destination = reverse_geo(lat2, lon1).replace(" ", "+")

    nav_request = "origin={}&destination={}&key={}".format(origin, destination, api_key)
    request = endpoint + nav_request
    response = json.loads(requests.get(request).text)

    route = [[lat1, lon1]]
    if len(response["routes"]) > 0:

        for x in response["routes"][0]["legs"][0]["steps"]:
            route.append([x["end_location"]["lat"], x["end_location"]["lng"]])

    route.append([lat2, lon2])

    return route


# print(get_route_points())


def get_distance(lat1, lon1, lat2, lon2):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

    origin = reverse_geo(lat1, lon1).replace(" ", "+")
    destination = reverse_geo(lat2, lon1).replace(" ", "+")

    nav_request = "origin={}&destination={}&key={}".format(origin, destination, api_key)
    request = endpoint + nav_request
    response = json.loads(requests.get(request).text)

    dist = 0

    if len(response["routes"]) == 0:
        return 0

    for x in response["routes"][0]["legs"][0]["steps"]:
        dist += x["distance"]["value"]

    return dist  # metros


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
