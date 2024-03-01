import folium
from folium import plugins
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from folium.plugins import FastMarkerCluster, MarkerCluster
import io 
import boto3 
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import json
import psycopg2

load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'dermod'

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

us_center = [37.0902, -95.7129]
m = folium.Map(location=us_center, zoom_start=4, zoom_control=False, scrollWheelZoom=True)

wind_group = folium.FeatureGroup(name='Wind Energy')
solar_group = folium.FeatureGroup(name='Utility-Scale Solar')
distr_solar_group = folium.FeatureGroup(name='Distributed Solar')

def create_marker(row, icon_color, popup_text):
    icon = folium.Icon(color=icon_color)
    marker = folium.Marker(location=(row["latitude"], row["longitude"]), icon=icon, popup=popup_text)
    return marker

resp_wind = s3_client.get_object(Bucket=bucket_name, Key='wind_energy_2.csv')
wind_data = resp_wind['Body'].read().decode('utf-8')
wind_df = pd.read_csv(io.StringIO(wind_data))
CAISO_wind = wind_df[wind_df["t_state"] == "CA"]
for _, row in CAISO_wind.iterrows():
    wind_group.add_child(create_marker(row, 'red', 'Individual Wind Turbine'))


resp_util_sol = s3_client.get_object(Bucket=bucket_name, Key='utility_solar (1).csv')
util_sol_data = resp_util_sol['Body'].read().decode('utf-8')
util_sol_df = pd.read_csv(io.StringIO(util_sol_data), on_bad_lines='skip', delimiter='\t')
CAISO_sol = util_sol_df[util_sol_df["state"] == "CA"]
for _, row in CAISO_sol.iterrows():
    solar_group.add_child(create_marker(row, 'blue', 'Utility-Scale Photovoltaic Power Station'))


resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
CAISO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')
max_cluster_distance = 5
for _, row in CAISO_coords_sol.iterrows():
    distr_solar_group.add_child(create_marker(row, 'green', 'Distributed Solar Unit'))

# Adding feature groups to the map
m.add_child(wind_group)
m.add_child(solar_group)
m.add_child(distr_solar_group)

# Adding layer control
folium.LayerControl().add_to(m)

# Save the map
m.save("map_CAISO.html")
