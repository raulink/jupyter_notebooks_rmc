import dash
from dash import dash_table
from dash import dcc  #import dash_core_components as dcc
from dash import html #import dash_html_components as html
#import dash_bootstrap_components as dbc
from dash import dcc, html

from pathlib import Path
import pandas as pd

from dash.dependencies import Input, Output, State
from dash import dcc, html, Input, Output, callback
import pandas as pd
from io import BytesIO
import base64
import os


#from pages.reportgenerator import *



# Crear la carpeta temp si no existe
# Inicializar la app de Dash con Bootstrap
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout2 = html.Div([
    html.H1("Sistema de Contrataciones"),
    
    # Botón para subir el archivo Excel
    dcc.Upload(
        id='upload-excel',
        children=html.Button('Subir Archivo Excel'),
        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    # Botón para generar el documento final
    html.Button("Generar Documento", id="generate-button", n_clicks=0, disabled=True),
    dcc.Download(id="download-docx"),
    
    # Mensaje de estado
    html.Div(id='output-state', style={'marginTop': 20})
])

print("Planes de Mantenimiento")

