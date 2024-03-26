import os, colorcet, param as pm, holoviews as hv, panel as pn, datashader as ds, pandas as pd, boto3, geopandas as gpd, gridstatus
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
        self.dimensions = [1300, 800]
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
        names = ['CAISO', 'PJM', 'NYISO', 'ISONE']
        self.multi_choice = pn.widgets.MultiChoice(name='MultiSelect',
            options=[i for i in names]).servable(target='sidebar')
        pn.Column(self.multi_choice, height=200)
        # self.multi_choice.param.watch(self.update_slider, 'value')

    def create_bokeh_plot(self):
        # Create your Bokeh plot here
        from bokeh.plotting import figure
        # caiso = gridstatus.CAISO()
        # caiso_load = caiso.get_load(start="Jan 1, 2021", end="Jan 10, 2021")
        # p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
        # p.line(caiso_load, legend_label="today load CAISO", line_width=2)

        p = figure(title="Bokeh Plot in Sidebar", width=self.dimensions[0], height=self.dimensions[1])
        p.circle([1, 2, 3, 4, 5], [3, 5, 7, 2, 1])

        # t_col = pn.Column(
        #     "Graph", p, 
        #     width=1300, 
        #     height=800
        #     ).servable(title="Bokeh Plot")
        # for i in self.multi_choice.value: 
        #     if i == 'CAISO':
        #         t_col.visible = False
        self.t_col = pn.Column(
            "Graph", p, 
            width=1300, 
            height=800, 
            visible=True
        ).servable(title="Bokeh Plot")
        return p
    
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
        shaded_plot.opts(width=self.dimensions[0], height=self.dimensions[1])
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
        # self.inside = None
        point_crs = {'init': 'epsg:4326'}
        x, y = event.xdata, event.ydata
        
        self.df_point = gpd.GeoDataFrame(geometry=[Point(x, y)], crs=point_crs)
        self.shp = gpd.read_file(self.shapefile)

        if self.shp.crs != point_crs: 
            print("Warning: CRS mismatch. Reprojecting point to match shapefile CRS.")
            self.df_point = self.df_point.to_crs(self.shp_data.crs)
        else: 
            self.df_point = gpd.GeoDataFrame(geometry=[Point(x, y)], crs=self.shp_data.crs)

        # for iso in self.ISOs:
        #     joined = gpd.sjoin(self.df_point, iso, how='inner')
        joined = gpd.sjoin(self.df_point, self.shp_data, how='inner') # FIXME: self.CAISO -> self.shp_data
        self.inside_iso = joined.shape[0] > 0
        self.status_text.value = ("You are within an ISO" if self.inside_iso else "You are not within an ISO")

    def plot_update(self, event): 
        for i in event.new: 
            if i == "CAISO": 
                self.t_col.visible = False
                return  # Exit the function once CAISO is found
        # If CAISO is not found, set y.visible to True
            else: 
                self.t_col.visible = True
    def gen_dashboard(self):       
        pn.extension()  
        self.toggles()
        shaded_plot = self.data()
        plot = pn.pane.HoloViews(shaded_plot).get_root()
        # plot.on_event(pn.EventName.MOUSE_MOVE, self.move) # -> has to be an issue with the cursor tracking. 
        bokeh_plot = self.create_bokeh_plot()


        dashboard = pn.Column(
            "## DER Mapping ",
            pn.pane.HoloViews(shaded_plot),
            # pn.pane.HoloViews(bokeh_plot),
            # bokeh_plot,
            self.status_text,
            align="center"
        ).servable(title="REBS DER Mapping")
        self.multi_choice.param.watch(self.plot_update, 'value')
        return dashboard # -> ? 
    
der_mapper = DERMapping()
dashboard = der_mapper.gen_dashboard()
# debug = der_mapper.move()

