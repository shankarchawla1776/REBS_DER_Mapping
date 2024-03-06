import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, numpy as np, io, matplotlib.pyplot as plt, boto3, json, geopandas as gpd
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
#next goal = geojson configuration
load_dotenv(Path(".env"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = 'der-data-rebs'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
resp_data = s3_client.get_object(Bucket=bucket_name, Key='transmission_lines.geojson')

hv.extension('bokeh', logo=False)
pn.extension(template='fast')

class DERMapping: 
    def __init__(self): 

        self.data_fetching = DataFetcher()
        self.map = OSM()
        self.checkboxes = []
        self.capacity_slider = pn.widgets.FloatSlider(
            name='Capacity', start=0, end=10, value=5
        ).servable(target='sidebar')
        self.pricing_slider = pn.widgets.FloatSlider(
            name='Price', start=0, end=1, value=0.5
        ).servable(target='sidebar')
    
    def fetch_data(self): 
        data = self.data_fetching.fetch_data(data="wind_turbines")
        df = pd.DataFrame(data, columns=['latitude', 'longitude'])
        df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])
        points = hv.Points(df, ['x', 'y'])
        decimated_points = decimate(points)
        shaded_plot = self.map * datashade(decimated_points, cmap=colorcet.kb)
        shaded_plot.opts(width=1450, height=800)
        return shaded_plot
     
    def toggles(self): 
        self.checkboxes = []
        self.der_names = ['Wind', 'Solar', 'Hydro', 'Geothermal', 'Nuclear', 'Biomass', 'Coal', 'Oil', 'Gas', 'Other']
        for i in self.der_names: 
            checkbox = pm.Boolean(default=True)
            checkbox = pn.widgets.Checkbox(name=i, value=True, sizing_mode='fixed', layout='column', width=400, height=40)
    
            self.checkboxes.append(checkbox)
        for j in self.checkboxes:
            j.servable(target='sidebar')

    def gen_dashboard(self):         
        self.toggles()
        shaded_plot = self.fetch_data()
        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            align="center"
        ).servable(title="DER")
        return dashboard
    

der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()


