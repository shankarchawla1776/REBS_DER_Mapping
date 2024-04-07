import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, boto3, geopandas as gpd, gridstatus, plotly.express as px
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
from actors.pricing import Prices
from bokeh.plotting import figure
from actors.graphs import Graphing

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
        self.dimensions = [800, 800]
        self.intro = pn.widgets.StaticText(name='Introduction', value="This is a project meant to serve as an expository collection of DER data accross the united states. All of the data seen here is availible on the project's GitHub repository with download instuctions in the README file.").servable(target='sidebar')
        self.instructions = pn.widgets.StaticText(name="Instructions", value="To view today's pricing data, select an ISO from the dropdown menu. To view DER data, select the checkboxes for the desired data types.").servable(target='sidebar')
        self.capacity_slider = pn.widgets.FloatSlider(
            name='Capacity', start=0, end=10, value=5
        ).servable(target='sidebar')

        self.pricing_slider = pn.widgets.FloatSlider(
            name='Price', start=0, end=1, value=0.5
        ).servable(target='sidebar')
        self.shapefile = 'shape_files/Independent_System_Operators.shp'
        self.d_types = ['distributed_solar', 'wind_turbines', 'utility_solar']
        self.status_text = pn.widgets.StaticText(name='Status', value='', width=200)
        self.shp_data = gpd.read_file('shape_files/Independent_System_Operators.shp') 
        self.CAISO = self.shp_data[self.shp_data['NAME'] == 'CALIFORNIA INDEPENDENT SYSTEM OPERATOR']
        self.PJM = self.shp_data[self.shp_data['NAME'] == 'PJM INTERCONNECTION, LLC']
        self.NYISO = self.shp_data[self.shp_data['NAME'] == 'NEW YORK INDEPENDENT SYSTEM OPERATOR']
        self.ISONE = self.shp_data[self.shp_data['NAME'] == 'ISO NEW ENGLAND INC.']
        self.ISOs = [self.CAISO, self.PJM, self.NYISO, self.ISONE]
        names = ['CAISO', 'PJM', 'NYISO', 'ISONE', 'MISO']
        self.multi_choice = pn.widgets.MultiChoice(name='Select one ISO',
            options=[i for i in names]).servable(target='sidebar')
        pn.Column(self.multi_choice, height=500)
        # self.multi_choice.param.watch(self.update_slider, 'value')

    def create_bokeh_plot(self):
        pn.extension('plotly')
        self.names = ['CAISO_prices', 'PJM_prices', 'NYISO_prices', 'ISONE_prices']
        access_graphs = Graphing() 
        self.working_isos = ['CAISO', 'NYISO', 'MISO']
        d = [] 
        for i in access_graphs.gen_graphs(iso=['CAISO', 'NYISO', 'MISO']):
            d.append(i)
        return d
    
    def data(self): 
        x = pd.DataFrame(columns=['latitude', 'longitude']) 
        self.d = []
        for query in self.d_types:
            df = self.data_fetching.fetch_data(data=query)
            df = pd.DataFrame(df, columns=['latitude', 'longitude'])
            self.d.append(df)
        combined_df = pd.concat([self.d[0], self.d[1]], ignore_index=True) # FIXME: for some reason, not every term is included.
        combined_df['x'], combined_df['y'] = lnglat_to_meters(combined_df['longitude'], combined_df['latitude'])
        points = hv.Points(combined_df, ['x', 'y'])
        decimated_points = decimate(points)
        shaded_plot = self.map * datashade(decimated_points, cmap='#560000')  # cmap=colorcet.kb)
        shaded_plot.opts(width=self.dimensions[0], height=self.dimensions[1], align="center")
        # shaded_plot.opts(width='100%', height='100%', sizing_mode='scale_both')

        return shaded_plot

    def toggles(self): 
        self.checkboxes = []
        for i in self.d_types: 
            checkbox = pm.Boolean(default=True)
            checkbox = pn.widgets.Checkbox(name=i, value=True, sizing_mode='fixed', width=400, height=40)
            self.checkboxes.append(checkbox)
        for j in self.checkboxes:
            j.servable(target='sidebar')
    
    def plot_update(self, event): 
        for j in self.create_bokeh_plot(): 
            j.visible = False
        for i in event.new: 
            if i == "CAISO": 
                x = self.create_bokeh_plot()
                x[0].visible = True
                return

            
    # def plot_update(self, event): 
    #     for i in event.new: 
    #         if i == "CAISO": 
    #             i.visible = True
    #             return
    #         elif i == "NYISO": 
    #             i.visible = True
    #             return
    #         elif i == "MISO":
    #             i.visible = True
    #             return

    def gen_dashboard(self):       
        pn.extension()  
        self.toggles()
        shaded_plot = self.data()
        plot = pn.pane.HoloViews(shaded_plot).get_root()

        for i in self.create_bokeh_plot(): 
            i.servable(title="Bokeh Plot")

        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            self.status_text,
            align="center"
        ).servable(title="REBS DER Mapping")
        self.multi_choice.param.watch(self.plot_update, 'value')
        return dashboard # -> ? 
    
der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()
# debug = der_mapper.move()

