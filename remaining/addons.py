import numpy as np
import pandas as pd
import geopy
import json  
from pandas import json_normalize
from geopy.geocoders import Nominatim 
import requests
from tabulate import tabulate
from sklearn.cluster import KMeans
import random
import folium
import openrouteservice as ors
import folium
import operator
from functools import reduce

location = 'Nellore'
city = location
## get location
locator = geopy.geocoders.Nominatim(user_agent="MyCoder")
location = locator.geocode(city)
print(location)
latpoint=location.latitude
longpoint=location.longitude
## keep latitude and longitude only
location = [location.latitude, location.longitude]
print("[lat, long]:", location)
print(latpoint,longpoint)

#retireving the data apartments 
url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r=10000&limit=100&q=resorts&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latpoint,longpoint)
data = requests.get(url).json()
d=json_normalize(data['items'])
d.to_csv('D:/jupyter/apartment.csv')


client = ors.Client(key='KTCJJ2YZ2143QHEZ2JAQS4FJIO5DLSDO0YN4YBXPMI5NKTEF')

# use self-hosted
# client = ors.Client(base_url='localhost:8080/ors')



m = folium.Map(location=list(reversed([-77.0362619, 38.897475])), tiles="cartodbpositron", zoom_start=13)

# white house to the pentagon
coords = [[-77.0362619, 38.897475], [-77.0584556, 38.871861]]

route = client.directions(coordinates=coords,
                          profile='foot-walking',
                          format='geojson')

waypoints = list(dict.fromkeys(reduce(operator.concat, list(map(lambda step: step['way_points'], route['features'][0]['properties']['segments'][0]['steps'])))))

folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']], color="blue").add_to(m)

folium.PolyLine(locations=[list(reversed(route['features'][0]['geometry']['coordinates'][index])) for index in waypoints], color="red").add_to(m)

m