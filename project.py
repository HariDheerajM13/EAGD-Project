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

def execute(location,preference1,preference2,preference3):
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

    #Retrieving the dataset of Apartments 
    url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r=10000&limit=100&q=apartment&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latpoint,longpoint)
    data = requests.get(url).json()
    d=json_normalize(data['items'])
    d.to_csv('D:/jupyter/apartment.csv')

    if d.empty or d['title'].count() < 3:
        map_emp=folium.Map(location=[latpoint,longpoint],zoom_start=12.5)
        folium.Marker([latpoint,longpoint],popup=city).add_to(map_emp)
        map_emp.save("D:/jupyter/templates/mapResult.html")
        return "This is empty one"
    else :
        #Cleaning API data
        d2=d[['title','address.label','distance','access','position.lat','position.lng','address.postalCode','id']]
        d2.to_csv('D:/jupyter/cleaned_apartment.csv')
        
        #Counting no. of Restaurants, department stores and gyms near apartments 
        df_final=d2[['position.lat','position.lng']]
        apartdata=d2[['title']]
        if(apartdata['title'].count() < 25):
            randomsample=apartdata
        else :
            randomsample=apartdata.sample(n=25)
            randomsample=randomsample.sort_values(by='title', ascending=True)
        RestList=[]
        DepList=[]
        GymList=[]
        latitudes = list(d2['position.lat'])
        longitudes = list( d2['position.lng'])
        for lat, lng in zip(latitudes, longitudes):    
            radius = '1500' #Set the radius to 1500 metres
            latitude=lat
            longitude=lng
            
            search_query = preference1 #Search for preference 1
            url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r={}&q={}&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latitude, longitude, radius, search_query)
            results = requests.get(url).json()
            venues=json_normalize(results['items'])
            venues.to_csv('D:/jupyter/restaurants.csv')
            if venues.empty:
                RestList.append(0)
            else:
                RestList.append(venues['title'].count())
            
            search_query = preference2 #Search for preference 2
            url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r={}&q={}&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latitude, longitude, radius, search_query)
            results = requests.get(url).json()
            venues=json_normalize(results['items'])
            venues.to_csv('D:/jupyter/gyms.csv')
            if venues.empty:
                DepList.append(0)
            else:
                DepList.append(venues['title'].count())

            search_query = preference3 #search for preference 3
            url = 'https://discover.search.hereapi.com/v1/discover?in=circle:{},{};r={}&q={}&apiKey=uJHMEjeagmFGldXp661-pDMf4R-PxvWIu7I68UjYC5Q'.format(latitude, longitude, radius, search_query)
            results = requests.get(url).json()
            venues=json_normalize(results['items'])
            venues.to_csv('D:/jupyter/grocerices.csv')
            if venues.empty:
                GymList.append(0)
            else:
                GymList.append(venues['title'].count())

        df_final['Restaurants'] = RestList
        df_final['Department Stores'] = DepList
        df_final['Gyms'] = GymList
        df_final.to_csv('D:/jupyter/ipDataforCluster.csv')

        #Run K-means clustering on dataframe
        kclusters = 3

        kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(df_final)
        df_final['Cluster']=kmeans.labels_
        df_final['Cluster']=df_final['Cluster'].apply(str)

        df_final.to_csv('D:/jupyter/clusterData.csv')
        

        #Plotting clustered locations on map using Folium

        #define coordinates of the user location
        map_bom=folium.Map(location=[latpoint,longpoint],zoom_start=12.5)

        # instantiate a feature group for the incidents in the dataframe
        locations = folium.map.FeatureGroup()

        # set color scheme for the clusters
        def color_producer(cluster):
            if cluster=='0':
                return 'green'
            elif cluster=='1':
                return 'blue'
            else:
                return 'red'

        latitudes = list(df_final['position.lat'])
        longitudes = list(df_final['position.lng'])
        labels = list(df_final['Cluster'])
        names=list(d2['title'])
        for lat, lng, label,names in zip(latitudes, longitudes, labels,names):
            folium.CircleMarker(
                    [lat,lng],
                    fill=True,
                    fill_opacity=0,
                    popup=folium.Popup(names, max_width = 300),
                    radius=8,
                    color=color_producer(label)
                ).add_to(map_bom)

        # add locations to map
        map_bom.add_child(locations)
        folium.Marker([latpoint,longpoint],popup=city).add_to(map_bom)

        #saving the map 
        map_bom.save("D:/jupyter/templates/mapResult.html")
        map_bom
        
        return randomsample