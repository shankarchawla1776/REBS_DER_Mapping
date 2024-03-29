import gridstatus 
import pandas as pd 
import panel as pn
import plotly.express as px
from actors.pricing import Prices

class Graphing: 

    def __init__(self): 
        self.CAISO = gridstatus.CAISO()
        self.NYISO = gridstatus.NYISO()
        self.dimensions = [2000, 1000]
        pass 
    
    def gen_graphs(self): 
        prices = Prices()
        CAISO = prices.get_CAISO_prices()
        NYISO = prices.get_NYISO_prices()
        def create_fig(iso): 
            fig = px.line(iso, x="Average LMP", y="Chunk", title=f"LMP Prices - Today in {iso}", width=self.dimensions[0], height=self.dimensions[1])
            return fig
        caiso_lmp = pn.Column(
            "Graph", create_fig(CAISO), 
            width=self.dimensions[0], 
            height=self.dimensions[1], 
            visible=False
        )
        nyiso_lmp = pn.Column(
            "Graph", create_fig(NYISO), 
            width=self.dimensions[0], 
            height=self.dimensions[1], 
            visible=False
        )
        ls = [caiso_lmp, nyiso_lmp]
        return ls
    
