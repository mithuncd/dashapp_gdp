# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

df = pd.read_csv('gdplifeexp2007.csv')

countries = df['country'].unique()

app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div([
    html.Div([
    html.Div([
        html.Label('Country'),
        dcc.Dropdown(
            id='country',
            options=[{'label': i, 'value': i} for i in countries],
            value='',
            placeholder='Select...',
            multi=True
        )
    ],
    className='twelve columns')
    ],className='row'
    #style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}
    ),
    html.Div([
    html.Div([
        html.Label('Life Expectancy'),
        dcc.Slider(
            id='expectancy-slider',
            min=30,
            max=80,
            value=30,
            step=None,
            marks={'30':'>30', '40':'>40', '50':'>50', '60':'>60', '70':'>70', '80':'>80'}
        ),
    ],
    className='twelve columns')
    ],className='row'),
    #style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '20px'}),

    html.Div([
    html.Div([
        dcc.Graph(id='life-exp-vs-gdp'),
    ],
    className='twelve columns',
        style={

            'margin-top': 20
        }
    )
    ],className='row')

],className='ten columns offset-by-one')

@app.callback(
    dash.dependencies.Output('life-exp-vs-gdp', 'figure'),
    [
        dash.dependencies.Input('expectancy-slider', 'value'),
        dash.dependencies.Input('country', 'value')
    ])
def update_graph(expectancy, country):

    filtered_df = df.loc[df["life expectancy"] > expectancy]

    if (country != '' and country is not None):
        filtered_df = filtered_df[df.country.str.contains('|'.join(country))]

    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdp per capita'],
            y=df_by_continent['life expectancy'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'GDP Per Capita', 'titlefont': dict(size=18, color='darkgrey'), 'zeroline': False, 'ticks': 'outside' },
            yaxis={'title': 'Life Expectancy', 'titlefont': dict(size=18, color='darkgrey'), 'range': [30, 90], 'ticks': 'outside'},
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }
if __name__ == '__main__':
    app.run_server()

#