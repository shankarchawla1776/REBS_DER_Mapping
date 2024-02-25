import folium
from folium import plugins
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from folium.plugins import FastMarkerCluster, HeatMap
import io 
import boto3 
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import psycopg2
from data_fetching.fetch_data import fetch_data




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


data = fetch_data()
data_1 = [36.501724, -99.787033], [36.437126, -99.725624], [36.444931, -99.769722], [36.513935, -99.80706], [36.444984, -99.758476], [36.431931, -99.772133], [36.489838, -99.740372], [36.476582, -99.810005], [36.454903, -99.762489], [36.502792, -99.761673], [36.485386, -99.776581], [36.491375, -99.724426], [36.490211, -99.714981], [36.490849, -99.70752], [36.429668, -99.760849], [36.448009, -99.745461], [36.489468, -99.733009], [36.488712, -99.750793], [36.48975, -99.814697], [36.432888, -99.742203], [36.498882, -99.737236], [36.423683, -99.741096], [36.433651, -99.781944], [36.503357, -99.796494], [36.451591, -99.733086], [36.445465, -99.775742], [36.421703, -99.724144], [36.44593, -99.786308], [36.435909, -99.737022], [36.429882, -99.776512], [36.50259, -99.741119], [36.423359, -99.735718], [36.515823, -99.762627], [36.451477, -99.74147], [36.476624, -99.804855], [36.474033, -99.792625], [36.476807, -99.788475], [36.440704, -99.799377], [36.438831, -99.79464], [36.491249, -99.756958], [36.44141, -99.790665], [36.424934, -99.720284], [36.424843, -99.714928], [36.473541, -99.782089], [36.517494, -99.821129], [36.513348, -99.744316], [36.44109, -99.731606], [36.502522, -99.778603], [36.484463, -99.782372], [36.515972, -99.826469], [36.446674, -99.751343], [36.428902, -99.752548], [36.458096, -99.775963], [36.440956, -99.764076], [36.513859, -99.812325]
# chunk_size = 1000
# chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
# heatmap = folium.plugins.HeatMap(data_1, radius=15, gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(m)
marker_cluster_wind = FastMarkerCluster(data=data_1, name='Individual Wind Turbines', callback=callback_0).add_to(m)


# marker_cluster_wind = FastMarkerCluster(data=data, name='Individual Wind Turbines', callback=callback_0).add_to(m)

# resp_wind = s3_client.get_object(Bucket=bucket_name, Key='wind_energy_2.csv')
# wind_data = resp_wind['Body'].read().decode('utf-8')
# wind_df = pd.read_csv(io.StringIO(wind_data))
# CAISO_wind = wind_df[wind_df["t_state"] == "CA"]
# xlong_values = CAISO_wind["xlong"].tolist()
# ylat_values = CAISO_wind["ylat"].tolist()
# locs_wind = CAISO_wind.apply(lambda row: (row["ylat"], row["xlong"]), axis=1).tolist()


# resp_util_sol = s3_client.get_object(Bucket=bucket_name, Key='utility_solar (1).csv')
# util_sol_data = resp_util_sol['Body'].read().decode('utf-8')
# util_sol_df = pd.read_csv(io.StringIO(util_sol_data), on_bad_lines='skip', delimiter='\t')
# CAISO_sol = util_sol_df[util_sol_df["state"] == "CA"]
# locs_sol = CAISO_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()



# resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
# distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
# CAISO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')
# lats_distr = CAISO_coords_sol["latitude"]
# longs_distr = CAISO_coords_sol["longitude"]
# locs_distr_sol = CAISO_coords_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()

# max_cluster_distance = 5


# marker_cluster_sol = FastMarkerCluster(data=locs_sol, name='Utility-Scale PV Stations', callback=callback_1).add_to(m)
# # marker_cluster_wind = FastMarkerCluster(data=locs_wind,  name='Individual Wind Turbines', callback=callback_0).add_to(m)
# marker_cluster_distr_sol = FastMarkerCluster(data=locs_distr_sol, callback=callback_2, name='Distributed Solar Units', options={'distance': max_cluster_distance}).add_to(m)



folium.LayerControl().add_to(m)
# m.add_child(marker_cluster_distr_sol)
# m.add_child(marker_cluster_wind)
# m.add_child(marker_cluster_sol)
m.save("map_1.html")

