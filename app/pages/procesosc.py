import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
import io
import pandas as pd

app = dash.Dash(__name__)

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

app.layout = layout

@app.callback(
    [Output('generate-button-2', 'disabled'),
     Output('output-state-2', 'children')],
    Input('upload-excel-2', 'contents')
)
def update_button_state(contents):
    if contents:        
        return False, "Archivo subido exitosamente."
    return True, ""

