import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, boto3, geopandas as gpd 
from holoviews.element import tiles as hvts
from holoviews.operation.datashader  import rasterize, shade, spread
from collections import OrderedDict as odict
from datashader.utils import lnglat_to_meters
from holoviews.operation import decimate
from holoviews.operation.datashader import datashade
from holoviews.element.tiles import EsriImagery, OSM, CartoLight
from dotenv import load_dotenv
from pathlib import Path
from data_fetching.fetch_data import DataFetcher
from shapely.geometry import Point 


checkboxes = []
#next goal = geojson configuration => consider creating one large data file with a column dedicated to type. this would be easier for toggles. 
#try .shp file
load_dotenv(Path(".env"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

hv.extension('bokeh', logo=False)
pn.extension(template='fast')

class DERMapping: 
    def __init__(self): 
        self.bucket_name = 'der-data-rebs'
        self.response = s3_client.get_object(Bucket=self.bucket_name, Key='DER_data/full_coordinates.csv')
        self.data_fetching = DataFetcher()
        self.map = OSM()
        self.checkboxes = []

        self.capacity_slider = pn.widgets.FloatSlider(
            name='Capacity', start=0, end=10, value=5
        ).servable(target='sidebar')

        self.pricing_slider = pn.widgets.FloatSlider(
            name='Price', start=0, end=1, value=0.5
        ).servable(target='sidebar')
       
        self.d_types = ['distributed_solar', 'wind_turbines', 'utility_solar']

    def data(self): 
        x = pd.DataFrame(columns=['latitude', 'longitude']) 
        self.d = []

        for query in self.d_types:
            df = self.data_fetching.fetch_data(data=query)
            df = pd.DataFrame(df, columns=['latitude', 'longitude'])
            self.d.append(df)

        # x = len(self.d)
        # for i in range(x):
            
        combined_df = pd.concat([self.d[0], self.d[1]], ignore_index=True) # FIXME: for some reason, not every term is included.
        # combined_df = pd.concat([self.d], ignore_index=True)
        combined_df['x'], combined_df['y'] = lnglat_to_meters(combined_df['longitude'], combined_df['latitude'])
        points = hv.Points(combined_df, ['x', 'y'])

        decimated_points = decimate(points)
        shaded_plot = self.map * datashade(decimated_points, cmap='#560000')  # cmap=colorcet.kb)
        shaded_plot.opts(width=1300, height=800)
        return shaded_plot
    
    def toggles(self): 
        self.checkboxes = []
        for i in self.d_types: 
            checkbox = pm.Boolean(default=True)
            checkbox = pn.widgets.Checkbox(name=i, value=True, sizing_mode='fixed', width=400, height=40)
            self.checkboxes.append(checkbox)
        for j in self.checkboxes:
            j.servable(target='sidebar')
    
    def move(self, event):

        self.shp_data = gpd.read_file('shape_files/Independent_System_Operators.shp') 
        self.CAISO = self.shp_data[self.shp_data['NAME'] == 'CALIFORNIA INDEPENDENT SYSTEM OPERATOR']
        self.PJM = self.shp_data[self.shp_data['NAME'] == 'PJM INTERCONNECTION, LLC']
        self.NYISO = self.shp_data[self.shp_data['NAME'] == 'NEW YORK INDEPENDENT SYSTEM OPERATOR']
        self.ISONE = self.shp_data[self.shp_data['NAME'] == 'ISO NEW ENGLAND INC.']
        self.ISOs = [self.CAISO, self.PJM, self.NYISO, self.ISONE]
        names = ['CAISO', 'PJM', 'NYISO', 'ISONE']
        self.inside = None
        point_crs = {'init': 'epsg:4326'}

        x, y = event.xdata, event.ydata
        # point = Point(x, y)
        # for iso in self.ISOs: 
        #     if iso.geometry.contains(point).any(): 
        #         print("You are inside an ISO")
        #         return
            
        if self.shp_data.crs != point_crs: 
            print("Warning: CRS mismatch. Reprojecting point to match shapefile CRS.")
            self.df_point = gpd.GeoDataFrame(geometry=[Point(x, y)], crs=point_crs)
            self.df_point = self.df_point.to_crs(self.shp_data.crs)
        else: 
            self.df_point = gpd.GeoDataFrame(geometry=[Point(x, y)], crs=point_crs)
        for iso in self.ISOs:
            joined = gpd.sjoin(self.df_point, iso, how='inner')

        if joined.shape[0] > 0: 
            self.inside = True
        else: 
            self.inside = False

        self.status_text = pn.widgets.StaticText(name='Status', value='You are not within an ISO', width=200)
        if self.inside: 
            self.status_text = pn.widgets.StaticText(name='Status', value='You are within an ISO', width=200)
        return self.status_text




    def gen_dashboard(self):         
        self.toggles()
        shaded_plot = self.data()
        plot = pn.pane.HoloViews(shaded_plot).get_root()
        
        plot.on_event('motion_notify_event', self.move)
        
        # self.status_text = pn.widgets.Text(name='Status', value='', width=200)
        text = self.move
        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            text,
            align="center"
        ).servable(title="REBS DER Mapping")
        return dashboard
    


der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()


