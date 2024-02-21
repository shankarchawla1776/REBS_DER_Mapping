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
import psycopg2


load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'dermod'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
us_center = [37.0902, -95.7129]
m = folium.Map(location=us_center, zoom_start=4, zoom_control = False, scrollWheelZoom=True)



callback_0 = """\
function (row) { 
    var icon, marker;
    icon = L.AwesomeMarkers.icon({
        icon: "map-marker", markerColor: "red"});
    marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.setIcon(icon);
    marker.bindPopup("Individual Wind Turbine")
    return marker;
};
"""
callback_1 = """
function (row) {
    var icon, marker;
    icon = L.AwesomeMarkers.icon({
        icon: "map-marker", markerColor: "blue"});
    marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.setIcon(icon);
    marker.bindPopup("Utility-Scale Photovoltaic Power Station ")
    return marker;
};
"""
callback_2 = """
function (row) {
    var icon, marker;
    icon = L.AwesomeMarkers.icon({
        icon: "sun", markerColor: "green"});
    marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.setIcon(icon);
    marker.bindPopup("Distributed Solar Unit")
    return marker;
};
"""

# def create_callback(marker_color, popup_text):
#     return """
#     function (row) { 
#         var icon, marker;
#         icon = L.AwesomeMarkers.icon({
#             icon: "map-marker", markerColor: "%s"});
#         marker = L.marker(new L.LatLng(row[0], row[1]));
#         marker.setIcon(icon);
#         marker.bindPopup("%s")
#         return marker;
#     };
#     """ % (marker_color, popup_text)

# callbacks = {
#     'Individual Wind Turbines': create_callback('red', 'Individual Wind Turbine'),
#     'Utility-Scale PV Stations': create_callback('blue', 'Utility-Scale Photovoltaic Power Station'),
#     'Distributed Solar Units': create_callback('green', 'Distributed Solar Unit')
# }

# def add_marker_cluster(map_obj, data, callback):
#     marker_cluster = FastMarkerCluster(data=data, callback=callback).add_to(map_obj)
#     return marker_cluster


resp_wind = s3_client.get_object(Bucket=bucket_name, Key='wind_energy_2.csv')
wind_data = resp_wind['Body'].read().decode('utf-8')
wind_df = pd.read_csv(io.StringIO(wind_data))
CAISO_wind = wind_df[wind_df["t_state"] == "CA"]
xlong_values = CAISO_wind["xlong"].tolist()
ylat_values = CAISO_wind["ylat"].tolist()
locs_wind = CAISO_wind.apply(lambda row: (row["ylat"], row["xlong"]), axis=1).tolist()


resp_util_sol = s3_client.get_object(Bucket=bucket_name, Key='utility_solar (1).csv')
util_sol_data = resp_util_sol['Body'].read().decode('utf-8')
util_sol_df = pd.read_csv(io.StringIO(util_sol_data), on_bad_lines='skip', delimiter='\t')
CAISO_sol = util_sol_df[util_sol_df["state"] == "CA"]
locs_sol = CAISO_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()



resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
CAISO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')
lats_distr = CAISO_coords_sol["latitude"]
longs_distr = CAISO_coords_sol["longitude"]
locs_distr_sol = CAISO_coords_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()

max_cluster_distance = 5

# for layer_name, callback in callbacks.items():
#     data = locals().get("locs_" + layer_name.lower().replace(' ', '_'))
#     if data:
#         add_marker_cluster(m, data, callback)

marker_cluster_sol = FastMarkerCluster(data=locs_sol, name='Utility-Scale PV Stations', callback=callback_1).add_to(m)
marker_cluster_wind = FastMarkerCluster(data=locs_wind,  name='Individual Wind Turbines', callback=callback_0).add_to(m)
marker_cluster_distr_sol = FastMarkerCluster(data=locs_distr_sol, callback=callback_2, name='Distributed Solar Units', options={'distance': max_cluster_distance}).add_to(m)



folium.LayerControl().add_to(m)
m.add_child(marker_cluster_distr_sol)
m.add_child(marker_cluster_wind)
m.add_child(marker_cluster_sol)
m.save("map_CAISO.html")

CAISO_sol = util_sol_df[util_sol_df["state"] == "CA"]

ylat = util_sol_df["latitude"].tolist()
