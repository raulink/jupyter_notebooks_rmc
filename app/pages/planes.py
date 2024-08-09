import dash

from dash import dash_table
from dash import dcc  #import dash_core_components as dcc
from dash import html #import dash_html_components as html
# import dash_bootstrap_components as dbc
from dash import dcc, html

from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate
from num2words import num2words


from dash.dependencies import Input, Output, State
import base64
import os
from docxtpl import DocxTemplate

from pages.reportgenerator import *


# Definir la función handle_uploads
def handle_uploads(excel_contents, excel_filename):
    messages = []
    if excel_contents:
        content_type, content_string = excel_contents.split(',')
        decoded = base64.b64decode(content_string)
        if not os.path.exists('temp'):
            os.makedirs('temp')
        path = os.path.join('temp', excel_filename)
        with open(path, 'wb') as f:
            f.write(decoded)
        messages.append(f"Archivo Excel {excel_filename} subido exitosamente.")
    return messages

# Layout de la aplicación
layout = html.Div([
    html.H1("Sistema de Contrataciones"),
    
    dcc.Upload(
        id='upload-excel-2',
        children=html.Button('Subir Archivo Excel'),
        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
        multiple=False
    ),
    
    html.Button("Generar Documento", id="generate-button-2", n_clicks=0, disabled=True),
    
    html.Div(id='output-state-2', style={'marginTop': 20})
])


# Callback para actualizar el estado del botón y manejar la subida del archivo
@callback(
    [Output('generate-button-2', 'disabled'),
     Output('output-state-2', 'children')],
    [Input('upload-excel-2', 'contents')],
    [State('upload-excel-2', 'filename')]
)
def update_button_state(contents, filename):
    if contents:
        messages = handle_uploads(contents, filename)
        return False, " ".join(messages)
    return True, ""





@callback(
    [Output('generate-button-2', 'disabled'),
     Output('output-state-2', 'children')],
    Input('upload-excel-2', 'contents')
)
def update_button_state(contents):
    if contents:        
        return False, "Archivo subido exitosamente."
    return True, ""

