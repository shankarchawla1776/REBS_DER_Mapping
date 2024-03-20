import pandas as pd
import geopandas as gpd
from shapely.geometry import Point  # Needed for point creation
import folium 

def is_point_in_shapefile(data_file, shapefile, latitude, longitude):
    df = pd.read_csv(data_file)

    try:
        df_shape = gpd.read_file(shapefile)
    except FileNotFoundError:
        print(f"Error: Shapefile '{shapefile}' not found.")
        return False

    point_crs = {'init': 'epsg:4326'} 
    if df_shape.crs != point_crs:
        print("Warning: CRS mismatch. Reprojecting point to match shapefile CRS.")
        df_point = gpd.GeoDataFrame(geometry=[Point(longitude, latitude)], crs=point_crs)
        df_point = df_point.to_crs(df_shape.crs)
    else:
        df_point = gpd.GeoDataFrame(geometry=[Point(longitude, latitude)], crs=df_shape.crs)

    joined = gpd.sjoin(df_point, df_shape, how='inner')

    if joined.shape[0] > 0:
        return True
    else:
        return False



data_file = 'shape_files/csv/Independent_System_Operator_-7181045740166301968 (1).csv'
shapefile = 'shape_files/Independent_System_Operators.shp'
latitude = 34.030149 
longitude = -118.178751 

if is_point_in_shapefile(data_file, shapefile, latitude, longitude):
  print("Your point is within a shape in the file.")
else:
  print("Your point is not within any shapes in the file.")

gdf_shape = gpd.read_file(shapefile)

m = folium.Map(location=[gdf_shape.centroid.y.mean(), gdf_shape.centroid.x.mean()], zoom_start=10)
folium.GeoJson(gdf_shape.to_json(), style_function=lambda feature: {
    'fillColor': 'green',
    'weight': 2,
    'opacity': 1
}).add_to(m)

marker = folium.Marker([latitude, latitude], popup='Selected Point')
marker.add_to(map)

m.add_child(folium.map.LayerControl())
m.save('map.html')
#34.030149,-118.178751