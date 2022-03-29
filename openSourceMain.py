import json
import pandas as pd
import requests
import json
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time

# convert json file to df
f = open("drivers.json")
json_drivers = json.load(f)
df_drivers = pd.DataFrame.from_dict(json_drivers)
#print(df_drivers)

f = open("locations.json")
json_locations = json.load(f)
df_locations = pd.DataFrame.from_dict(json_locations)
#print(df_locations)

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248d78346ffbd314936809ae8a93c99522a',
    'Content-Type': 'application/json; charset=utf-8'
}

def get_distance(lon1, lat1, lon2, lat2):
    nav_request =  {"coordinates":[[lat1,lon1],[lat2,lon2]]}
    endpoint = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=nav_request, headers=headers)
    response = endpoint.json()
    dist = 0
    time.sleep(1.5)
    if endpoint.status_code == 200:
        dist = response["routes"][0]["summary"]["distance"]
    print(endpoint)
    return dist

#print(get_distance(40.518348,-3.897235,40.519669,-3.900518))

def get_route_points(lat1, lon1, lat2, lon2):

    nav_request =  {"coordinates":[[lat1,lon1],[lat2,lon2]]}
    endpoint = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=nav_request, headers=headers)
    response = endpoint.json()
  
    route = [[lat1,lon1]]

    if endpoint.status_code == 200:
        for x in response['routes'][0]['segments'][0]["steps"]:
            route.append( [ x['end_location']['lat'], x['end_location']['lng'] ])
    
    route.append([lat2, lon2])

    return route

def create_distance_matrix(latList, lonList):

    n = len(latList)

    M = np.zeros(shape=(n, n))

    for i in range(n):
        for j in range(i + 1, n):
            print(latList[i])
            print(lonList[i])
            print(latList[j])
            print(lonList[j])
            dist = get_distance(latList[i], lonList[i], latList[j], lonList[j])
            print(dist)
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
    data["distance_matrix"] = pd.read_csv('distance_matrix.csv', sep=',')
    #data["distance_matrix"] = create_distance_matrix(lat_combined, lng_combined)
    #pd.DataFrame(data["distance_matrix"]).to_csv("distance_matrix.csv", header=None, index=False)
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

  manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'], data['ends'])
  
  routing = pywrapcp.RoutingModel(manager)

  # Constante distancia
  def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

  transit_callback_index = routing.RegisterTransitCallback(distance_callback)

  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


  # Constante capacidad
  def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

  demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
  
  routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # slack
        data['vehicle_capacities'],  # Maximas Capacidades
        True,  # Empezar a acumular desde 0
        'Capacity')

  # Heuristica
  search_parameters = pywrapcp.DefaultRoutingSearchParameters()
  search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
  search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
  search_parameters.time_limit.FromSeconds(1)

  # Solucionar el problema
  solution = routing.SolveWithParameters(search_parameters)

  return (solution, manager, routing)

solution, manager, routing = get_solution(data)

print(solution)