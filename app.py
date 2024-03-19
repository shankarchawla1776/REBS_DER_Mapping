import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, boto3, gridstatus, geopandas as gpd, fiona 
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
from bokeh.models import GeoJSONDataSource
from shapely.geometry import Point
from bokeh.io import show 

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
        # self.
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
    
        if event.x is not None and event.y is not None:
            x, y = event.x, event.y
            # lon, lat = lnglat_to_meters.invert(x, y)
            point = Point(x, y)
            # for iso_name, iso_polygon in zip(["CAISO", "PJM", "NYISO", "ISONE"], self.ISOs):
            for iso_polygon in self.ISOs:
                if iso_polygon.geometry.contains(point).any():
                    # print(f"You are inside") 
                    tooltip_text = f"You are inside {iso_polygon['NAME'].values[0]}"
                    self.plot.hover.tooltips = [(tooltip_text, "@x, @y")]
                    return
        else:
            self.plot.hover.tooltips = None

    def gen_dashboard(self):         
        self.toggles()
        shaded_plot = self.data()
        plot = pn.pane.HoloViews(shaded_plot).get_root()

        plot.on_event('motion_notify_event', self.move)
        # self.status_text = pn.widgets.Text(name='Status', value='', width=200)

        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            # self.status_text,
            align="center"
        ).servable(title="REBS DER Mapping")
        return dashboard
    


der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()

