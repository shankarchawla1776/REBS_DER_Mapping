import folium
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from folium.plugins import FastMarkerCluster, MarkerCluster
import io 
import boto3 
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(Path("/my/path/.env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'dermod'

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

resp_wind = s3_client.get_object(Bucket=bucket_name, Key='wind_energy_2.csv')
wind_data = resp_wind['Body'].read().decode('utf-8')
wind_df = pd.read_csv(io.StringIO(wind_data))


us_center = [37.0902, -95.7129]

m = folium.Map(location=us_center, zoom_start=4, zoom_control = False, scrollWheelZoom=True)
#wind 
# wind_df = pd.read_csv("data/wind_energy_2.csv")


CASIO_wind = wind_df[wind_df["t_state"] == "CA"]

xlong_values = CASIO_wind["xlong"].tolist()

ylat_values = CASIO_wind["ylat"].tolist()

locs_wind = CASIO_wind.apply(lambda row: (row["ylat"], row["xlong"]), axis=1).tolist()

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
#util solar

resp_util_sol = s3_client.get_object(Bucket=bucket_name, Key='utility_solar (1).csv')
util_sol_data = resp_util_sol['Body'].read().decode('utf-8')
util_sol_df = pd.read_csv(io.StringIO(util_sol_data), on_bad_lines='skip', delimiter='\t')

CAISO_geojson = s3_client.get_object(Bucket=bucket_name, Key='CA (1).geojson')
CAISO_geojson_data = CAISO_geojson['Body'].read().decode('utf-8')
geojson_data = CAISO_geojson_data['Body'].read().decode('utf-8')

# print(util_sol_df.head())

# util_sol_df = pd.read_csv("data/utility_solar (1).csv", delimiter='\t')

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

CASIO_sol = util_sol_df[util_sol_df["state"] == "CA"]
locs_sol = CASIO_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()

marker_cluster_sol = FastMarkerCluster(data=locs_sol, callback=callback_1).add_to(m)



marker_cluster_wind = FastMarkerCluster(data=locs_wind, callback=callback_0).add_to(m)

resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
CASIO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')

# CASIO_coords_sol = pd.read_csv("data/CAISO_data/CASIO_coords.csv")

lats_distr = CASIO_coords_sol["latitude"]
longs_distr = CASIO_coords_sol["longitude"]

# def create_clusters(locations, callback, max_distance):
#     clusters = []
#     for loc in locations:
#         added_to_cluster = False
#         for cluster in clusters:
#             if all(np.linalg.norm(np.array(loc) - np.array(cluster)) < max_distance for cluster in clusters):
#                 cluster.append(loc)
#                 added_to_cluster = True
#                 break
#         if not added_to_cluster:
#             clusters.append([loc])
#     marker_cluster = FastMarkerCluster(data=clusters, callback=callback).add_to(m)
#     return marker_cluster


max_cluster_distance = 5

locs_distr_sol = CASIO_coords_sol.apply(lambda row: (row["latitude"], row["longitude"]), axis=1).tolist()


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

marker_cluster_distr_sol = FastMarkerCluster(data=locs_distr_sol, callback=callback_2, options={'distance': max_cluster_distance}).add_to(m)

# california_geojson = {
#     "type": "Feature",
#     "geometry": {
#         "type": "Polygon",
#         "coordinates": [[
#             [-125, 32],
#             [-114, 32],
#             [-114, 37],
#             [-125, 37],
#             [-125, 32]
#         ]]
#     },
#     "properties": {
#         "name": "California"
#     }
# }
 
# def on_geojson_click(feature, layer):
#     # You can customize the HTML content as needed
#     html_content = "<div style='position: absolute; top: 10px; right: 10px; background-color: white; padding: 10px;'>California Information</div>"
#     m.get_root().html.add_child(folium.Element(html_content))

# # Add GeoJSON layer to the map
# folium.GeoJson(california_geojson,
#                name="California",
#                style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue'},
#                highlight_function=lambda x: {'fillColor': '#ff0000', 'color': '#0000ff'},
#                tooltip="California",
#                on_each_feature=on_geojson_click  # Add this line
#                ).add_to(m)


def on_map_click(event):
    lat, lon = event.latlng
    popup_text = f"Clicked at: ({lat}, {lon})"
    
    popup = folium.Popup(popup_text, max_width=300)
    marker = folium.Marker([lat, lon], popup=popup)
    
    m.add_child(marker)

# Attach the click event handler to the map
m.add_click_for_marker(on_map_click)

m.add_child(marker_cluster_distr_sol)
m.add_child(marker_cluster_wind)
m.add_child(marker_cluster_sol)
m.save("map_w_CAISO_click.html")

CASIO_sol = util_sol_df[util_sol_df["state"] == "CA"]

ylat = util_sol_df["latitude"].tolist()
