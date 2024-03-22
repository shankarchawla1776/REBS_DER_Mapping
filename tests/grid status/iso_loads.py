import holoviews as hv
import pandas as pd
from datetime import datetime
import gridstatus

hv.extension('bokeh')

caiso = gridstatus.CAISO() 

caiso_load = caiso.get_load(start="Jan 1, 2021", end="Feb 1, 2021")

curve = hv.Curve(caiso_load)

# plot = curve.opts(
#     title='CAISO Load from Jan 1, 2021, to Feb 1, 2021',
#     xlabel='Date',
#     ylabel='Load (MW)',
#     width=800,
#     height=400,
#     show_grid=True
# ) 

# hv.save(plot, 'caiso_load_plot.html')

df = pd.DataFrame(caiso_load, columns=['timestamp', 'load'])
df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Calculate the average load
average_load = df['load'].mean()
str_avg = str(average_load)
print(caiso_load.mean())
                                  