import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dash import dcc, html, Input, Output, callback
import dash
# Configuración para acceder a Google Sheetseste 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('yopi-434514-02cae6081f5c.json', scope)
client = gspread.authorize(creds)

# ID del documento de Google Sheets
SHEET_ID = '1KdAnEDH4_lv6UMnUB_diVn3MFQdoYvEGE0LQcxXZ1-Y'

# Función para obtener los datos desde Google Sheets usando el ID del documento
def obtener_datos_desde_google_sheets(sheet_name, rango):
    hoja = client.open_by_key(SHEET_ID).worksheet(sheet_name)
    datos = hoja.get(rango)
    if not datos or len(datos) <= 1:
        print(f"No se encontraron datos en el rango {rango}")
        return pd.DataFrame()  # Retornar un DataFrame vacío
    df = pd.DataFrame(datos[1:], columns=datos[0])  # Ignorar la primera fila (encabezados)
    return df

# Función para convertir los datos de porcentajes de texto a númerosre
def convertir_porcentajes(df):
    if not df.empty:
        for col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace(',', '.').str.strip(), errors='coerce')
    return df

# Definir las opciones de tiempo
time_options = ['MENSUAL', 'BIMENSUAL', 'TRIMESTRAL', 'BALANCÍN MECÁNICO', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# Asignar colores de forma dinámica para cada periodo y categoría
categorias_base = ['AMARILLO', 'ROJA', 'AZUL', 'CELESTE', 'VERDE', 'BLANCO', 'NARANJA', 
                   'PLATEADA', 'MORADAS1', 'MORADAS2', 'CAFE']
colores_base = ['yellow', 'red', 'blue', 'lightblue', 'green', 'white', 'orange', 
                'silver', 'purple', 'purple', 'brown']
periodos = ['MENSUAL', 'BIMENSUAL', 'TRIMESTRAL','BALANCÍN MECÁNICO', 'BALANCÍN ELÉCTRICO','ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# Crear el diccionario de colores
color_dict = {f'{periodo} {categoria}': color for periodo in periodos for categoria, color in zip(categorias_base, colores_base)}

# Layout de la aplicación
layout = html.Div([
    html.H1('DASHBOARD DE INDICADORES DE TOREES'),

    html.Div([
        html.Label('Seleccione el periodo:'),
        dcc.Dropdown(
            id='tiempo-dropdown-1',
            options=[{'label': periodo, 'value': periodo} for periodo in time_options],
            value='MENSUAL'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Div([
        html.Label('Seleccione las graficas por 1 colores:'),
        dcc.Checklist(
            id='categoria-checklist-1',
            options=[],
            value=[],
            inline=True,
        )
    ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='dashboard-1')
    ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
])

# Callback para actualizar las opciones del checklist basado en la selección de tiempo
@callback(
    Output('categoria-checklist-1', 'options'),
    [Input('tiempo-dropdown-1', 'value')]
)
def update_checklist(selected_time):
    # Aquí obtenemos los datos más recientes de Google Sheets cada vez que se selecciona un periodo
    df = convertir_porcentajes(obtener_datos_desde_google_sheets('Hoja', {
        'MENSUAL': 'D7:N8',
        'BIMENSUAL': 'Q7:AA8',
        'TRIMESTRAL': 'AD7:AN8',
        'BALANCÍN MECÁNICO': 'AQ7:BA8',
        'BALANCÍN ELÉCTRICO': 'BD7:BN8',
        'ANUAL MECÁNICO': 'BQ7:CA8',
        'ANUAL ELÉCTRICO': 'CD7:CN8'
    }.get(selected_time, '')))

    if df.empty:
        print(f"No hay datos para el periodo {selected_time}.")
        return []

    options = [{'label': col, 'value': col} for col in df.columns]
    return options

# Callback para actualizar el dashboard basado en la selección del tiempo y categorías
@callback(
    Output('dashboard-1', 'figure'),
    [Input('tiempo-dropdown-1', 'value'),
     Input('categoria-checklist-1', 'value')]
)
def update_dashboard(selected_time, selected_categories):
    # Aquí obtenemos los datos más recientes de Google Sheets cada vez que el dashboard se actualiza
    df = convertir_porcentajes(obtener_datos_desde_google_sheets('Hoja', {
        'MENSUAL': 'D7:N8',
        'BIMENSUAL': 'Q7:AA8',
        'TRIMESTRAL': 'AD7:AN8',
        'BALANCÍN MECÁNICO': 'AQ7:BA8',
        'BALANCÍN ELÉCTRICO': 'BD7:BN8',
        'ANUAL MECÁNICO': 'BQ7:CA8',
        'ANUAL ELÉCTRICO': 'CD7:CN8'
    }.get(selected_time, '')))

    if not df.empty:
        if not selected_categories:
            selected_categories = df.columns

        try:
            # Filtrar las categorías seleccionadas
            fila_filtrada = df[selected_categories].iloc[0]

            df_temp = pd.DataFrame({
                'Categoría': fila_filtrada.index,
                'Porcentaje': fila_filtrada.values
            })

            # Normalizar los nombres de las categorías para evitar discrepancias
            df_temp['Categoría'] = df_temp['Categoría'].str.strip().str.upper()

            # Asignar colores basados en los nombres de las categorías
            df_temp['Color'] = df_temp['Categoría'].map(lambda x: color_dict.get(x, 'gray'))

            fig = px.bar(df_temp, x='Categoría', y='Porcentaje',
                         labels={'Categoría': 'Categoría', 'Porcentaje': 'Porcentaje'},
                         title=f'oficial2 - {selected_time}',
                         color='Categoría',
                         color_discrete_map=color_dict
                        )
            fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
            fig.update_layout(yaxis=dict(range=[0, 100]))
        except Exception as e:
            print(f"Error al crear el gráfico: {e}")
            fig = px.bar(title='Error al crear el gráfico')
    else:
        fig = px.bar(title='Sin datos disponibles')

#hh
    return fig