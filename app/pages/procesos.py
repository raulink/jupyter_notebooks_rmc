import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
from io import BytesIO
import base64
import os
from dash.dependencies import State
import dash_bootstrap_components as dbc

# Asegúrate de que este import sea correcto según la ubicación de tu clase
from planes.googleSheetProcesor import GoogleSheetProcessor

from pages.reportgenerator import *



# Crear la carpeta temp si no existe
# Inicializar la app de Dash con Bootstrap
# Crear la carpeta temp si no existe
if not os.path.exists('temp'):
    os.makedirs('temp')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([
    html.H1("Sistema de Contrataciones"),
    
    # Botón para subir el archivo Excel
    dcc.Upload(
        id='upload-excel-1',
        children=html.Button('Subir Archivo Excel'),
        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    # Botón para subir la plantilla de Word
    dcc.Upload(
        id='upload-template-1',
        children=html.Button('Subir Plantilla'),
        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    # Botón para generar el documento final
    html.Button("Generar Documento", id="generate-button-1", n_clicks=0, disabled=True),
    dcc.Download(id="download-docx-1"),
    
    # Mensaje de estado
    html.Div(id='output-state-1', style={'marginTop': 20})
])


@callback(
    [Output('generate-button-1', 'disabled'), Output('output-state-1', 'children')],
    [Input('upload-excel-1', 'contents'), Input('upload-template-1', 'contents')],
    [State('upload-excel-1', 'filename'), State('upload-template-1', 'filename')]
)
def handle_uploads(excel_contents, template_contents, excel_filename, template_filename):
    messages = []
    if excel_contents:
        content_type, content_string = excel_contents.split(',')
        decoded = base64.b64decode(content_string)
        path = os.path.join('temp', excel_filename)
        with open(path, 'wb') as f:
            f.write(decoded)
        messages.append(f"Archivo Excel {excel_filename} subido exitosamente.")
    
    if template_contents:
        content_type, content_string = template_contents.split(',')
        decoded = base64.b64decode(content_string)
        path = os.path.join('temp', template_filename)
        with open(path, 'wb') as f:
            f.write(decoded)
        #messages.append(f"\nPlantilla Word {template_filename} subida exitosamente.")
    if excel_contents and template_contents:
        return False, " ".join(messages)
    else:
        return True, " ".join(messages)
@callback(
    Output('download-docx-1', 'data'),
    [Input('generate-button-1', 'n_clicks')],
    [State('upload-excel-1', 'filename'), State('upload-template-1', 'filename')]
)
def download_excel(n_clicks, excel_filename, template_filename):
    if isinstance(n_clicks, int) and n_clicks > 0:
        # Ruta donde se guardará el archivo
        processed_file_path = os.path.join('temp', 'processed_output.xlsx')
        
        # Lógica para generar el archivo
        download_excel(excel_filename, template_filename, processed_file_path)

        # Verifica si el archivo existe antes de permitir la descarga
        if os.path.exists(processed_file_path):
            return dcc.send_file(processed_file_path)
        else:
            return "Error: El archivo no se ha generado."
    return None


