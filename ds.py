import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import lnglat_to_meters
from data_fetching.fetch_data import fetch_data
import colorcet 
import matplotlib.pyplot as plt
from datashader import export


data = fetch_data(wind=True) 

df = pd.DataFrame(data, columns=['ylat', 'xlong'])
cvs = ds.Canvas(plot_width=850, plot_height=1200)
agg = cvs.points(df, 'ylat', 'xlong')
img = ds.tf.shade(agg, cmap=colorcet.fire, how='log')



plt.figure(figsize=(10, 10))
plt.imshow(img, aspect='auto')
plt.axis('off')
plt.show()