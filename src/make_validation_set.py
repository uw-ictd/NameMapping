import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import haversine
import Levenshtein as lv
import dask.dataframe as dd

%matplotlib inline

osm_data = pd.read_csv('osm_data.csv')
osm_data = osm_data[osm_data['lon'] > -5]


renacom_data = pd.read_csv('~/data/data_niger_election_data/processed/renacom_full.csv', encoding =  "ISO-8859-1")
renaloc_data = pd.read_csv('~/data/data_niger_election_data/processed/renaloc_full.csv', encoding = "ISO-8859-1")
renacom_data.LATITUDE = pd.to_numeric(renacom_data.LATITUDE, errors='coerce')
renacom_data.LONGITUDE = pd.to_numeric(renacom_data.LONGITUDE, errors='coerce')
renacom_data = renacom_data[~(pd.isnull(renacom_data.LATITUDE))]


#Standardize data
renacom_data.LOCALITE = renacom_data.LOCALITE.str.lower()
osm_data['name'] = osm_data['name'].str.lower()

def distance_to_set(point, data_set, data_set_name , data_set_lat, data_set_long, max_distance):
    gps_point = (point.lat.iloc[0], point.lon.iloc[0])
    name_point = point.iloc[0]['name']
    data_set = haversine_point_to_set(data_set, data_set_lat, data_set_long, data_set_name,  gps_point, name_point)
    data_set = data_set[data_set['distance'] < max_distance]
    data_set['levenshtein'] = 0
    for n in range(len(data_set)):
        data_set['levenshtein'].iloc[n] = lv.distance(name_point, data_set[data_set_name].iloc[n])
    data_set['osm_name'] =  name_point
    return data_set[['osm_name','LOCALITE','distance','levenshtein']]

def haversine_point_to_set(data_set, data_set_lat, data_set_long, data_set_name, point_gps, point_name):
    gps_data_set = (data_set[data_set_lat], data_set[data_set_long])
    data_set['distance'] = haversine.distance(point_gps, gps_data_set)
    return data_set

osm_data.columns = ['id','lat','lon','name']

%%time
dists = osm_data.groupby('id').apply(distance_to_set, renacom_data, 'LOCALITE' ,'LATITUDE', 'LONGITUDE', 40)

dists = dists.sort_values(['distance', 'levenshtein'])

dists.to_csv('osm_renacome_distances_under40km.csv')
