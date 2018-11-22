import configparser
import json

import plotly
import plotly.plotly as py

conf = configparser.ConfigParser()
conf.read('praw.ini')

data = json.load(open('sankey.json'))

plotly.tools.set_credentials_file(username=conf.get('Plotly', 'PLOTLY_USERNAME'),
                                  api_key=conf.get('Plotly', 'PLOTLY_KEY'))

data_trace = dict(
    type='sankey',
    width=1118,
    height=772,
    domain=dict(
        x=[0, 1],
        y=[0, 1]
    ),
    orientation="h",
    valueformat=".0f",
    valuesuffix="TWh",
    node=dict(
        pad=15,
        thickness=15,
        line=dict(
            color="black",
            width=0.5
        ),
        label=data['data'][0]['node']['label'],
        color=data['data'][0]['node']['color']
    ),
    link=dict(
        source=data['data'][0]['link']['source'],
        target=data['data'][0]['link']['target'],
        value=data['data'][0]['link']['value'],
        label=data['data'][0]['link']['label']
    ))

layout = dict(
    title="Breakdown of subreddits names",
    font=dict(
        size=10
    )
)

fig = dict(data=[data_trace], layout=layout)
py.plot(fig, validate=False)
