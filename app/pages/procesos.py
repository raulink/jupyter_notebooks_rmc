import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
from io import BytesIO
import base64
import os
from dash.dependencies import State
# Asegúrate de que este import sea correcto según la ubicación de tu clase
from planes.googleSheetProcesor import GoogleSheetProcessor

# Inicializar la app de Dash
app = dash.Dash(__name__)

layout = html.Div([
    html.H1("Sistema de Procesamiento de Google Sheets"),

    # Botón para subir la URL de Google Sheet
    dcc.Input(
        id='sheet-url', type='text', placeholder='https://docs.google.com/spreadsheets/d/1OkECu7qNfGZxX_rc2RDbaz0A-oE_gUwJ0P2tjU_x-q0/edit?gid=1199302294#gid=1199302294', style={'width': '100%', 'margin': '10px'},    
    ),
    html.Button('Procesar Google Sheet', id='process-sheet', n_clicks=0),

    # Mensaje de estado
    html.Div(id='output-state', style={'marginTop': 20}),

    # Botón para descargar el archivo Excel generado
    html.Button("Descargar Archivo Excel", id="download-button",
                n_clicks=0, disabled=True),
    dcc.Download(id="download-excel")
])


@app.callback(
    [Output('download-button', 'disabled'),
     Output('output-state', 'children')],
    [Input('process-sheet', 'n_clicks')],
    [State('sheet-url', 'value')]
)
def handle_processing(n_clicks, sheet_url):
    if n_clicks > 0 and sheet_url:
        try:
            processor = GoogleSheetProcessor(sheet_url)
            processor.process_data()
            processor.save_to_excel('processed_output.xlsx')
            return False, "Procesamiento exitoso. Puede descargar el archivo Excel."
        except Exception as e:
            return True, f"Error en el procesamiento: {e}"
    return True, "Ingrese una URL de Google Sheet válida y haga clic en procesar."


@app.callback(
    Output('download-excel', 'data'),
    [Input('download-button', 'n_clicks')]
)
def download_excel(n_clicks):
    if n_clicks > 0:
        return dcc.send_file('processed_output.xlsx')
    return None


if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
