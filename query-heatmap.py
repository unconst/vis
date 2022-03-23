from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from base64 import b64encode
import io
import numpy as np
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import os

app = Dash(__name__)

def respond_time_heatmap():
    result = pd.read_json('data/queries/block-973062_batch-10_seq-20.txt')
    result = result.transpose()
    times = result['time'].to_numpy()
    times = times.reshape((40,50))
    times = pd.DataFrame(times)
    fig = px.imshow(
        times, 
        color_continuous_scale='Greens', 
        text_auto=True, 
        aspect="auto",
    )
    fig.update(data=[{'hovertemplate': 'UID: 50x%{y} + %{x}'}])
    fig.update_layout( width = 2000, height = 2000)
    fig.update_layout(
        margin=dict(l=0,r=0,b=0,t=0),
    )
    return fig


app.layout = html.Div(children=[
    html.H1(children='\nBlock height:\t{}'.format(973062)),
    html.H1(children='\nBatch size:\t{}'.format(10)),
    html.H1(children='\nSequence length:\t{}'.format(20)),
    dcc.Graph(id="dummy-respond-time-heatmap", figure = respond_time_heatmap() ),
])


if __name__ == '__main__':
    app.run_server(debug=False)
