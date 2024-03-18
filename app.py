import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, boto3, gridstatus
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
        combined_df = pd.concat([self.d[0], self.d[1]], ignore_index=True) # FIXME: for some reason, not every term is included. => Set up pricing API then come back. 
        # combined_df = pd.concat([self.d], ignore_index=True)
        combined_df['x'], combined_df['y'] = lnglat_to_meters(combined_df['longitude'], combined_df['latitude'])
        points = hv.Points(combined_df, ['x', 'y'])
        print(combined_df.head())
        decimated_points = decimate(points)
        shaded_plot = self.map * datashade(decimated_points, cmap='#560000')  # cmap=colorcet.kb)
        shaded_plot.opts(width=1450, height=800)
        return shaded_plot
    
    def toggles(self): 
        self.checkboxes = []
        for i in self.d_types: 
            checkbox = pm.Boolean(default=True)
            checkbox = pn.widgets.Checkbox(name=i, value=True, sizing_mode='fixed', layout='column', width=400, height=40)
            self.checkboxes.append(checkbox)
        for j in self.checkboxes:
            j.servable(target='sidebar')

    def gen_dashboard(self):         
        self.toggles()
        shaded_plot = self.data()
        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            align="center"
        ).servable(title="REBS DER Mapping")
        return dashboard
    
    # def gsconfig(self): 


der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()