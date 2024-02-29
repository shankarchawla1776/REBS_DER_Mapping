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

hv.extension('bokeh', logo=False)
data = fetch_data(wind=True)
df = pd.DataFrame(data, columns=['latitude', 'longitude'])
df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])
points = hv.Points(df, ['x', 'y'])
decimated_points = decimate(points)

map = EsriImagery()

# Create a shaded plot
# shaded_plot = shade(decimated_points, cmap=colorcet.fire)
shaded_plot = map * datashade(points, cmap=colorcet.fire)

shaded_plot.opts(width=1000, height=800)

dashboard = pn.Column(
    "## DER Mapping ",
    pn.pane.HoloViews(shaded_plot),
    align="center" 
)
pn.extension(template='fast')

freq = pn.widgets.FloatSlider(
    name='Capacity', start=0, end=10, value=5
).servable(target='sidebar')

ampl = pn.widgets.FloatSlider(
    name='Price', start=0, end=1, value=0.5
).servable(target='sidebar')

dashboard.servable()