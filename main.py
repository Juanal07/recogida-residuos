import json
import pandas as pd
import requests
import json
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

api_key = "AIzaSyAMot24WThCTr8aJCBRlvLzrUrrmqhKLlM"

# convert json file to df
f = open("data/drivers.json")
json_drivers = json.load(f)
df_drivers = pd.DataFrame.from_dict(json_drivers)
# print(df_drivers)

f = open("data/locations.json")
json_locations = json.load(f)
df_locations = pd.DataFrame.from_dict(json_locations)
# print(df_locations)


def get_distance(lat1, lon1, lat2, lon2):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

    nav_request = "origin={},{}&destination={},{}&key={}".format(
        lat1, lon1, lat2, lon2, api_key
    )
    request = endpoint + nav_request
    response = json.loads(requests.get(request).text)

    dist = 0

    if len(response["routes"]) == 0:
        return 0

    for x in response["routes"][0]["legs"][0]["steps"]:
        dist += x["distance"]["value"]

    return dist  # metros


def get_route_points(lat1, lon1, lat2, lon2):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

    nav_request = "origin={},{}&destination={},{}&key={}".format(
        lat1, lon1, lat2, lon2, api_key
    )
    request = endpoint + nav_request
    response = json.loads(requests.get(request).text)

    route = [[lat1, lon1]]

    if len(response["routes"]) > 0:
        for x in response["routes"][0]["legs"][0]["steps"]:
            route.append([x["end_location"]["lat"], x["end_location"]["lng"]])

    route.append([lat2, lon2])
    return route


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
    data["distance_matrix"] = pd.read_csv(
        "distance_matrix_final_py.csv", sep=",", header=None
    ).values.tolist()
    # data["distance_matrix"] = create_distance_matrix(lat_combined, lng_combined)
    # pd.DataFrame(data["distance_matrix"]).to_csv("distance_matrix_final_py.csv", header=None, index=False)
    print(data["distance_matrix"])
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


data = create_model(df_drivers, df_locations)
print(data)


def get_solution(data):

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["starts"], data["ends"]
    )

    routing = pywrapcp.RoutingModel(manager)

    # Constante distancia
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Constante capacidad
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # slack
        data["vehicle_capacities"],  # Maximas Capacidades
        True,  # Empezar a acumular desde 0
        "Capacity",
    )

    # Heuristica
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solucionar el problema
    solution = routing.SolveWithParameters(search_parameters)
    print(f"Objective: {solution.ObjectiveValue()}")
    return (solution, manager, routing)


solution, manager, routing = get_solution(data)
