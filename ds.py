import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import lnglat_to_meters
from data_fetching.fetch_data import fetch_data


df = fetch_data()

df['x'], df['y'] = lnglat_to_meters(df['longitude'], df['latitude'])

cvs = ds.Canvas(plot_width=1000, plot_height=1000)
agg = cvs.points(df, 'x', 'y')

img = tf.shade(agg, cmap=["blue"], how='log')
img = tf.set_background(img, "black")
img.to_pil().save("plot.png")

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Datashader Plot</title>
</head>
<body>
    <img src="plot.png" alt="Datashader Plot">
</body>
</html>
"""
with open("plot.html", "w") as html_file:
    html_file.write(html_content)
