import pandas as pd
import plotly.express as px
import panel as pn
import gridstatus

caiso = gridstatus.CAISO()
caiso_load = caiso.get_load(start=s, end=e)  # Replace s and e with your desired start and end times
fig = px.line(caiso_load, x="Time", y="Load")

responsive = pn.pane.Plotly(fig)

pn.Column(
    '# CAISO Load',
    responsive,
    sizing_mode='stretch_width'
).servable()

pn.Row(
    responsive.controls(jslink=True),
    responsive
).servable()

