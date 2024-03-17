from h3 import h3
import folium
import pandas as pd
from folium.plugins import FastMarkerCluster

geoJson1 = {'type': 'Polygon', 'coordinates': [[[90,-180],[90,0],[-90,0],[-90,-180]]]}
geoJson2 = {'type': 'Polygon', 'coordinates': [[[90,0],[90,180],[-90,180],[-90,0]]]}

hexagons = list(h3.polyfill(geoJson1, 1)) + list(h3.polyfill(geoJson2, 1))

polylines = []
for hex in hexagons:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    polylines.append(polyline)


"""
Define data with a file containing latitude and longitude coordinates.
"""

base = folium.Map([0,0], zoom_start=2, tiles='cartodbpositron')


for polyline in polylines:
    m = folium.PolyLine(locations=polyline, weight=1, color='black')
    base.add_child(m)
markers = []
for index, row in data.iterrows():
    marker = folium.Marker(
        location=[row['latitude'], row['longitude']],

    )
    markers.append(marker)

print(f"Number of wind turbines: {len(markers)}")
lat, lon = 40.7128, -74.0059 
hexagon_of_interest = h3.geo_to_h3(lat, lon, 12) 
print(f"Hexagon of interest: {hexagon_of_interest}")

"""
Random Corrdinates Chosen to test.
"""
latitude = 39.8333 
longitude = -98.5833
desired_resolution = 1  
hexagon_of_interest = h3.geo_to_h3(latitude, longitude, desired_resolution)


turbines_in_hexagon = [
    marker
    for marker in markers
    if h3.geo_to_h3(marker.location[0], marker.location[1], desired_resolution) == hexagon_of_interest
]

print(f"Number of wind turbines in the hexagon: {len(turbines_in_hexagon)}")
marker_cluster = FastMarkerCluster(
    data=[(marker.location[0], marker.location[1]) for marker in turbines_in_hexagon]
)
base.add_child(marker_cluster)

"""
Save to HTML output. 
It should be noted that Folium is not a good implementation for 
this method at scale. A similar approach would work with DataShader.
"""

"""
Data Output with data from DER_data/wind_turbines.csv: 
Number of wind turbines: 73351
Hexagon of interest: 8c2a107289061ff
Number of wind turbines in the hexagon: 13205
"""