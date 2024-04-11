import gridstatus 
import pandas as pd 
import panel as pn
import plotly.express as px
from .pricing import Prices

class Graphing: 

    def __init__(self): 
        pass

    def gen_graphs(self, iso=[]): 

        def create_fig(iso_for_fig): 
            fig = px.line(iso_for_fig, x="Average LMP", y="Chunk", title=f"LMP Prices - Today in {iso}", width=self.dimensions[0], height=self.dimensions[1])
            return fig
        
        d = [] 
        prices = Prices()
        self.CAISO = prices.get_CAISO_prices()
        self.NYISO = prices.get_NYISO_prices()
        self.MISO = prices.get_MISO_prices()
        self.dimensions = [800, 800]
        self.caiso_lmp = None
        self.nyiso_lmp = None
        self.miso_lmp = None

        for i in iso: 
                dict = {"CAISO": self.CAISO, "NYISO": self.NYISO, "MISO": self.MISO}
                for key, value in dict.items():
                    if i == key: 
                        d.append(create_fig(value))
        return d 

    
x = Graphing()
y = x.gen_graphs(iso=["CAISO", "NYISO", "MISO"])
print(y)


        # for i in iso: 
        #     if i == "CAISO": 
        #         self.caiso_lmp = pn.Column(
        #             "Graph", create_fig(self.CAISO), 
        #             width=self.dimensions[0], 
        #             height=self.dimensions[1], 
        #             visible=False
        #         )
        #         d.append(self.caiso_lmp)
        #     elif i == "NYISO": 
        #         self.nyiso_lmp = pn.Column(
        #             "Graph", create_fig(self.NYISO), 
        #             width=self.dimensions[0], 
        #             height=self.dimensions[1], 
        #             visible=False
        #         )
        #         d.append(self.nyiso_lmp)
        #     elif i == "MISO": 
        #         self.miso_lmp = pn.Column(
        #             "Graph", create_fig(self.MISO), 
        #             width=self.dimensions[0], 
        #             height=self.dimensions[1], 
        #             visible=False
        #         )