import dash
from dash import html
import dash_core_components as dcc
from dash import dcc
import os
#import psycopg2

# Conexión a la base de datos PostgreSQL
#conn = psycopg2.connect(
#    host="db",
#    database="mydatabase",
#    user="postgres",
#    password="password"
#)

# Crear una aplicación Dash
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Inicio Dash'),

    html.Div(children='''
        Primera aplicacion Dashboard
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [1, 2, 3, 4, 5], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3, 4, 5], 'y': [10, 9, 8, 7, 6], 'type': 'bar', 'name': 'NYC'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
