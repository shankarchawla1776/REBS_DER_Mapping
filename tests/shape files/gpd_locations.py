import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import mplcursors

data = gpd.read_file('shape_files/Independent_System_Operators.shp')

print(data['NAME'])
california_data = data[data['NAME'] == 'CALIFORNIA INDEPENDENT SYSTEM OPERATOR']

ax = data.plot()

def on_move(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        point = Point(x, y)  
        if california_data.geometry.contains(point).any():  
            # print(f"Latitude: {y}, Longitude: {x}")
            # mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text("?"))
            print(x, y)

plt.connect('motion_notify_event', on_move)

plt.show()

