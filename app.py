import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, numpy as np, io, matplotlib.pyplot as plt, boto3
from holoviews.element import tiles as hvts
from holoviews.operation.datashader import rasterize, shade, spread
from collections import OrderedDict as odict
from datashader.utils import lnglat_to_meters
from holoviews.operation import decimate
from holoviews.operation.datashader import datashade
from holoviews.element.tiles import EsriImagery, OSM, CartoLight
from dotenv import load_dotenv
from pathlib import Path


ds_count = 10 
checkboxes = []
load_dotenv(Path(".env"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name = 'dermod'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

resp_distr_sol = s3_client.get_object(Bucket=bucket_name, Key='CASIO_coords.csv')
distr_sol_data = resp_distr_sol['Body'].read().decode('utf-8')
CAISO_coords_sol = pd.read_csv(io.StringIO(distr_sol_data), on_bad_lines='skip')

hv.extension('bokeh', logo=False)

def update_opacity(active, alpha):
    if active:
        return alpha
    else:
        return 0

alpha_values = [0.8] * ds_count

def update_plot(*checkbox_values):
    alpha = [update_opacity(active, alpha) for active, alpha in zip(checkbox_values, alpha_values)]
    decimated_combined_points.opts(alpha=alpha)

d_names = ['Wind', 'Solar', 'Hydro', 'Geothermal', 'Nuclear', 'Biomass', 'Coal', 'Oil', 'Gas', 'Other']


for i in range(ds_count): 
    d_types = pn.widgets.Checkbox(name=d_names[i], value=True, sizing_mode='fixed', layout='column', width=400, height=40)
    checkboxes.append(d_types)

for i in checkboxes:
    pn.Row(i.controls(jslink=True), i)

data = fetch_data(wind=True)
data2 = CAISO_coords_sol
dfs = [pd.DataFrame(data, columns=['latitude', 'longitude']), 
              pd.DataFrame(data2, columns=['latitude', 'longitude'])]
              
df1 = pd.DataFrame(data, columns=['latitude', 'longitude'])
df2 = pd.DataFrame(data2, columns=['latitude', 'longitude'])

df1['x'], df1['y'] = lnglat_to_meters(df1['longitude'], df1['latitude'])

df2['x'], df2['y'] = lnglat_to_meters(df2['longitude'], df2['latitude'])


points_combined = pd.concat([df1, df2])
combined_points = hv.Points(points_combined, ['x', 'y'])


decimated_combined_points = decimate(combined_points)
decimated_combined_points.opts(alpha=0.8)
map = OSM()

shaded_plot = map * datashade(decimated_combined_points, cmap=colorcet.kb) # => ,cmap=colorcet.fire

shaded_plot.opts(width=1250, height=800)

dashboard = pn.Column(
    "## DER Mapping ",
    pn.pane.HoloViews(shaded_plot),
    # stream2_visibility,
    align="center" 
)
pn.extension(template='fast')

capacity = pn.widgets.FloatSlider(
    name='Capacity', start=0, end=10, value=5
).servable(target='sidebar')

pricing = pn.widgets.FloatSlider(
    name='Price', start=0, end=1, value=0.5
).servable(target='sidebar')



for i in checkboxes: 
    checkbox_column = pn.Column(*checkboxes, align='center')
    i.servable(target='sidebar')
          
dashboard.servable(title="Distributed Energy Resources Mapping")


# def toggle_stream2_visibility(active):
#     if active:
#         shaded_plot = map * datashade(points, cmap=colorcet.fire) * datashade(points2, cmap=colorcet.fire)
#     else:
#         shaded_plot = map * datashade(points, cmap=colorcet.fire)
#     pn.pane.HoloViews(shaded_plot).servable()

