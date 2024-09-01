import os
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc  # Importar dash-bootstrap-components
import plotly.express as px
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los detalles de la conexión desde el archivo .env
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Crear la URL de conexión
connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

# Crear el motor de conexión con SQLAlchemy
engine = create_engine(connection_string)

# Cargar datos desde la tabla 'ingreso' en un DataFrame
df = pd.read_sql('SELECT * FROM ingreso;', engine)

# Convertir la columna 'fecha_ingreso' a tipo de datos datetime
df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], dayfirst=True)

# Obtener opciones únicas para el combobox de 'codigo_item', 'descripcion' y 'anio'
codigo_item_options = [{'label': item, 'value': item} for item in df['codigo_item'].unique()]
descripcion_options = [{'label': desc, 'value': desc} for desc in df['descripcion'].unique()]
anio_options = [{'label': str(anio), 'value': anio} for anio in df['fecha_ingreso'].dt.year.unique()]

# Agregar el selector de tipo de gráfico en el diseño
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Código de Ítem"),
            dcc.Dropdown(
                id='codigo-item-dropdown',
                options=codigo_item_options,
                placeholder='Selecciona un código de ítem',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Descripción"),
            dcc.Dropdown(
                id='descripcion-dropdown',
                options=descripcion_options,
                placeholder='Selecciona una descripción',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Año"),
            dcc.Dropdown(
                id='anio-dropdown',
                options=anio_options,
                placeholder='Selecciona un año',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Tipo de Gráfico"),
            dcc.Dropdown(
                id='tipo-grafico-dropdown',
                options=[
                    {'label': 'Gráfico de Barras Apiladas', 'value': 'barras_apiladas'},
                    {'label': 'Gráfico de Columnas Apiladas', 'value': 'columnas_apiladas'},
                    {'label': 'Gráfico de Barras Agrupadas', 'value': 'barras_agrupadas'},
                    {'label': 'Gráfico de Columnas Agrupadas', 'value': 'columnas_agrupadas'},
                    {'label': 'Gráfico de Líneas', 'value': 'lineas'},
                    {'label': 'Gráfico de Cintas', 'value': 'cintas'},
                    {'label': 'Gráfico Circular', 'value': 'circular'},
                    {'label': 'Gráfico de Anillos', 'value': 'anillos'},
                    {'label': 'Gráfico de Area', 'value': 'area'}
                ],
                placeholder='Selecciona un tipo de gráfico',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-chart1'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P(id='suma-cantidad-label', style={'font-weight': 'bold'}),
            html.P(id='precio-unitario-maximo-label', style={'font-weight': 'bold'})
        ]),
        dbc.Col([
            dbc.Label("Rango de Fechas"),
            dcc.DatePickerRange(
                id='date-picker-range2',
                min_date_allowed=df['fecha_ingreso'].min().date(),
                max_date_allowed=df['fecha_ingreso'].max().date(),
                start_date=df['fecha_ingreso'].min().date(),
                end_date=df['fecha_ingreso'].max().date(),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
        ], width=6),
        
    ])
    
], fluid=True)


# Crear gráfico inicial sin filtro
fig = px.line(df, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)

# Callback para actualizar el gráfico y las etiquetas según las selecciones
@callback(
    [
        Output('line-chart1', 'figure'),
        Output('suma-cantidad-label', 'children'),
        Output('precio-unitario-maximo-label', 'children')
    ],
    [
        Input('codigo-item-dropdown', 'value'),
        Input('descripcion-dropdown', 'value'),
        Input('date-picker-range2', 'start_date'),
        Input('date-picker-range2', 'end_date'),
        Input('anio-dropdown', 'value'),
        Input('tipo-grafico-dropdown', 'value')  # Nuevo input para el tipo de gráfico
    ]
)
def update_graph(codigo_item, descripcion, start_date, end_date, anio, tipo_grafico):
    # Crear una copia del DataFrame original para filtrar
    df_filtrado = df.copy()

    # Filtrar datos según el 'codigo_item' seleccionado
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    
    # Filtrar datos según la 'descripcion' seleccionada
    if descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]
        
    # Filtrar datos según la 'fecha_ingreso' seleccionada
    if start_date and end_date:
        df_filtrado = df_filtrado[(df_filtrado['fecha_ingreso'] >= start_date) & (df_filtrado['fecha_ingreso'] <= end_date)]
    
    # Filtrar datos según el 'anio' seleccionado
    if anio:
        df_filtrado = df_filtrado[df_filtrado['fecha_ingreso'].dt.year == int(anio)]

    # Crear gráfico según el tipo seleccionado
    if tipo_grafico == 'barras_apiladas':
        fig = px.bar(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', text='cantidad', 
                    color='descripcion', barmode='stack')
    elif tipo_grafico == 'columnas_apiladas':
        fig = px.bar(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', text='cantidad', 
                    color='descripcion', barmode='stack', orientation='v')
    elif tipo_grafico == 'barras_agrupadas':
        fig = px.bar(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', text='cantidad', 
                    color='descripcion', barmode='group')
    elif tipo_grafico == 'columnas_agrupadas':
        fig = px.bar(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', text='cantidad', 
                    color='descripcion', barmode='group', orientation='v')
    elif tipo_grafico == 'lineas':
        fig = px.line(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)
    elif tipo_grafico == 'cintas':
        fig = px.treemap(df_filtrado, path=['descripcion'], values='cantidad', title='Cantidad por descripción')
    elif tipo_grafico == 'circular':
        fig = px.pie(df_filtrado, names='descripcion', values='cantidad', title='Distribución de cantidades')
    elif tipo_grafico == 'anillos':
        fig = px.pie(df_filtrado, names='descripcion', values='cantidad', title='Distribución de cantidades', hole=0.3)
    elif tipo_grafico == 'area':
        fig = px.area(df_filtrado, x='fecha_ingreso', y='cantidad', color='ubicacion', title='Cantidad por fecha de ingreso')
    
    else:
        # Default to line chart if no type selected
        fig = px.line(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)

    # Calcular la suma de cantidades
    suma_cantidad = df_filtrado['cantidad'].sum()

    # Calcular el precio unitario máximo si existe la columna 'precio_unitario'
    if 'precio_unitario' in df_filtrado.columns:
        precio_unitario_maximo = df_filtrado['precio_unitario'].max()
    else:
        precio_unitario_maximo = None

    # Formatear los resultados como cadenas de texto para mostrarlos en las etiquetas
    suma_cantidad_label = f"Suma de cantidades: {suma_cantidad}"
    precio_unitario_maximo_label = f"Precio unitario máximo: {precio_unitario_maximo}" if precio_unitario_maximo else "Precio unitario máximo: N/A"

    # Retornar el gráfico y las etiquetas de resultados
    return fig, suma_cantidad_label, precio_unitario_maximo_label
# Código principal de la aplicación
if __name__ == '__main__':
    external_stylesheets = [dbc.themes.BOOTSTRAP]  # Usar un tema de Bootstrap
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
    app.layout = layout
    app.run_server(debug=False, host='0.0.0.0', port=8080)
