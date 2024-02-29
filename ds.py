import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds
import intake
from holoviews.element import tiles as hvts
from holoviews.operation.datashader import rasterize, shade, spread
from collections import OrderedDict as odict
from data_fetching.fetch_data import fetch_data
from datashader.utils import lnglat_to_meters
from holoviews.operation import decimate
import pandas as pd 
from holoviews.operation.datashader import datashade
import matplotlib.pyplot as plt
import numpy as np 
from holoviews.element.tiles import EsriImagery
from dotenv import load_dotenv
import boto3 
from pathlib import Path
import io 
# from map_gen.main import CAISO_coords_sol

load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'dermod'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
CAISO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')

hv.extension('bokeh', logo=False)
data = fetch_data(wind=True)
data2 = CAISO_coords_sol
df = pd.DataFrame(data, columns=['latitude', 'longitude'])
df2 = pd.DataFrame(data2, columns=['latitude', 'longitude'])
df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])
df2['x'], df2['y'] = lnglat_to_meters(df2['longitude'], df2['latitude'])

points = hv.Points(df, ['x', 'y'])
points2 = hv.Points(df2, ['x', 'y'])

decimated_points = decimate(points)
# decimated_points2 = decimate(points2)
map = EsriImagery()

# Create a shaded plot
# shaded_plot = shade(decimated_points, cmap=colorcet.fire)
shaded_plot = map * datashade(points, cmap=colorcet.fire)

shaded_plot.opts(width=1000, height=800)

stream2_visibility = pn.widgets.Checkbox(name='Show Solar', value=True)

def toggle_stream2_visibility(active):
    if active:
        shaded_plot.options(overlay_dims=['stream2'])
    else:
        shaded_plot.options(overlay_dims=[])

# Add the callback function to the widget
stream2_visibility.param.watch(toggle_stream2_visibility, 'value')




dashboard = pn.Column(
    "## DER Mapping ",
    pn.pane.HoloViews(shaded_plot),
    stream2_visibility,
    align="center" 
)
pn.extension(template='fast')

capacity = pn.widgets.FloatSlider(
    name='Capacity', start=0, end=10, value=5
).servable(target='sidebar')

pricing = pn.widgets.FloatSlider(
    name='Price', start=0, end=1, value=0.5
).servable(target='sidebar')

dashboard.servable(title="Dsitributed Energy Resources Mapping")