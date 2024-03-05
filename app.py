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
from data_fetching.fetch_data import DataFetcher


ds_count = 10
act_count = 3
checkboxes = []
hv.extension('bokeh', logo=False)


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
        self.der_names = ['Wind', 'Solar', 'Hydro', 'Geothermal', 'Nuclear', 'Biomass', 'Coal', 'Oil', 'Gas', 'Other']

    def fetch_data(self): 
        data = self.data_fetching.fetch_data(data="wind_turbines")
        df = pd.DataFrame(data, columns=['latitude', 'longitude'])
        df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])
        points = hv.Points(df, ['x', 'y'])
        decimated_points = decimate(points)
        shaded_plot = self.map * datashade(decimated_points, cmap=colorcet.kb)
        shaded_plot.opts(width=1250, height=800)
        return shaded_plot
     
    def toggles(self): 
        for name in self.der_names: 
            checkbox = pn.widgets.Checkbox(name=name, value=True, sizing_mode='fixed', layout='column', width=400, height=40)
            self.checkboxes.append(checkbox)
        return self.checkboxes

    def sidebar(self): 
        sidebar = pn.Column(
            "## DER Mapping ",
            self.capacity_slider, 
            self.pricing_slider, 
            pn.Spacer(height=20),
            pn.Column(*self.checkboxes, align='center'),
            align="center"
        )
        return sidebar
    
    def gen_dashboard(self): 
        self.toggles()
        shaded_plot = self.fetch_data()
        sidebar = self.sidebar()
        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            # sidebar,
            align="center"
        )
        pn.extension(template='fast')
        dashboard.servable(title="Distributed Energy Resources Mapping")
        return dashboard

der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()

# der_mapper.gen_dashboard()







# hv.extension('bokeh', logo=False)
# data_fetcher = DataFetcher()


# d_names = ['Wind', 'Solar', 'Hydro', 'Geothermal', 'Nuclear', 'Biomass', 'Coal', 'Oil', 'Gas', 'Other']


# for i in range(ds_count): 
#     d_types = pn.widgets.Checkbox(name=d_names[i], value=True, sizing_mode='fixed', layout='column', width=400, height=40)
#     checkboxes.append(d_types)

# for i in checkboxes:
#     pn.Row(i.controls(jslink=True), i)


# dfs = []

# data = data_fetcher.fetch_data(data="wind_turbines")
# dfs.append(pd.DataFrame(data, columns=['latitude', 'longitude']))

# df1, df2, df3 = dfs

# for df in [df1, df2, df3]:
#     df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])

# points_combined = pd.concat(dfs)
# combined_points = hv.Points(points_combined, ['x', 'y'])


# decimated_combined_points = decimate(combined_points)
# decimated_combined_points.opts(alpha=0.8)
# map = OSM()

# shaded_plot = map * datashade(decimated_combined_points, cmap=colorcet.kb) # => ,cmap=colorcet.fire

# shaded_plot.opts(width=1250, height=800)

# dashboard = pn.Column(
#     "## DER Mapping ",
#     pn.pane.HoloViews(shaded_plot),
#     # stream2_visibility,
#     align="center" 
# )
# pn.extension(template='fast')

# capacity = pn.widgets.FloatSlider(
#     name='Capacity', start=0, end=10, value=5
# ).servable(target='sidebar')

# pricing = pn.widgets.FloatSlider(
#     name='Price', start=0, end=1, value=0.5
# ).servable(target='sidebar')



# for i in checkboxes: 
#     checkbox_column = pn.Column(*checkboxes, align='center')
#     i.servable(target='sidebar')
          
# dashboard.servable(title="Distributed Energy Resources Mapping")


# # def toggle_stream2_visibility(active):
# #     if active:
# #         shaded_plot = map * datashade(points, cmap=colorcet.fire) * datashade(points2, cmap=colorcet.fire)
# #     else:
# #         shaded_plot = map * datashade(points, cmap=colorcet.fire)
# #     pn.pane.HoloViews(shaded_plot).servable()

# # def update_opacity(active, alpha):
# #     if active:
# #         return alpha
# #     else:
# #         return 0

# # alpha_values = [0.8] * ds_count

# # def update_plot(*checkbox_values):
# #     alpha = [update_opacity(active, alpha) for active, alpha in zip(checkbox_values, alpha_values)]
# #     decimated_combined_points.opts(alpha=alpha)

# # load_dotenv(Path(".env"))

# # AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# # AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# # bucket_name = 'der-data-rebs'
# # s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# # keys = ['DER_data/battery_storage.csv', 'DER_data/distributed_solar.csv', 'DER_data/utility_solar.csv']
# # datasets = {} 
# # for i, key in enumerate(keys):
# #     var_name = f"dataset_{i+1}"
# #     resp_data = s3_client.get_object(Bucket=bucket_name, Key=key)
# #     data = resp_data['Body'].read().decode('utf-8')

# #     datasets[var_name] = pd.read_csv(io.StringIO(data), on_bad_lines='skip')