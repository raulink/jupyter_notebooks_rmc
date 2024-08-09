import dash

from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from io import BytesIO
import base64

app = dash.Dash(__name__)

class FileHandler:
    def __init__(self):
        self.dataframe = None

    def parse_contents(self, contents, filename):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                self.dataframe = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename or 'xlsx' in filename:
                self.dataframe = pd.read_excel(io.BytesIO(decoded))
            else:
                return None
        except Exception as e:
            print(e)
            return None
        return self.dataframe

    def get_download_link(self):
        if self.dataframe is not None:
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            self.dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.save()
            output.seek(0)
            encoded = base64.b64encode(output.read()).decode('utf-8')
            return f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{encoded}'
        return None

file_handler = FileHandler()

layout2 = html.Div([
=======
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import base64
import os

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

        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'}
    ),
    
    html.Button("Generar Documento", id="generate-button-2", n_clicks=0, disabled=True),
    dcc.Download(id="download-docx-2"),
        style={'width': '100%', 'height': '70px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
        multiple=False
    ),
    
    html.Button("Generar Documento", id="generate-button-2", n_clicks=0, disabled=True),

    
    html.Div(id='output-state-2', style={'marginTop': 20})
])


app.layout = layout2

@app.callback(
    Output('generate-button-2', 'disabled'),
    Input('upload-excel-2', 'contents')
)
def update_button_state(contents):
    if contents is not None:
        return False
    return True

@app.callback(
    Output('download-docx-2', 'data'),
    Input('generate-button-2', 'n_clicks'),
    State('upload-excel-2', 'contents'),
    State('upload-excel-2', 'filename')
)
def generate_document(n_clicks, contents, filename):
    if n_clicks > 0 and contents is not None:
        df = file_handler.parse_contents(contents, filename)
        if df is not None:
            return dict(content=file_handler.get_download_link(), filename=filename)
    return None

if __name__ == '__main__':
    app.run_server(debug=True)

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