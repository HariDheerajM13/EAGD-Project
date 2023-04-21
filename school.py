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

def schools(location):
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
    url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r=10000&limit=100&q=school&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latpoint,longpoint)
    data = requests.get(url).json()
    d=json_normalize(data['items'])
    d.to_csv('D:/jupyter/apartment.csv')

    if d.empty or d['title'].count() < 3:
        map_rest=folium.Map(location=[latpoint,longpoint],zoom_start=12.5)
        folium.Marker([latpoint,longpoint],popup=city).add_to(map_rest)
        map_rest.save("D:/jupyter/templates/schlmapResult.html")
        return "This is empty one"
    else :
        map_rest=folium.Map(location=[latpoint,longpoint],zoom_start=15)
        latitudes = list(d['position.lat'])
        longitudes = list(d['position.lng'])
        names=list(d['title'])
        for lat, lng, names in zip(latitudes, longitudes, names):
            folium.CircleMarker(
                    [lat,lng],
                    fill=True,
                    fill_opacity=0,
                    popup=folium.Popup(names, max_width = 300),
                    radius=8,
                    color='red'
                ).add_to(map_rest)
        folium.Marker([latpoint,longpoint],popup=city).add_to(map_rest)
        map_rest.save("D:/jupyter/templates/schlmapResult.html")
        return "Done"