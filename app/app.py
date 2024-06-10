import dash
from dash import html
import os
import psycopg2

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="db",
    database="mydatabase",
    user="postgres",
    password="password"
)

# Crear una aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
