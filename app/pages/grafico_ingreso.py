import os
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import io
import plotly.io as pio
import plotly.graph_objects as go

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

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Agregar el selector de tipo de gráfico en el diseño
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Código de Ítem"),
            dcc.Dropdown(
                id='codigo-item-dropdown1',
                options=codigo_item_options,
                placeholder='Selecciona un código de ítem',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Descripción"),
            dcc.Dropdown(
                id='descripcion-dropdown1',
                options=descripcion_options,
                placeholder='Selecciona una descripción',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Año"),
            dcc.Dropdown(
                id='anio-dropdown1',
                options=anio_options,
                placeholder='Selecciona un año',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Tipo de Gráfico"),
            dcc.Dropdown(
                id='tipo-grafico-dropdown1',
                options=[
                    {'label': 'Gráfico de Barras Apiladas', 'value': 'barras_apiladas'},
                    {'label': 'Gráfico de Columnas Apiladas', 'value': 'columnas_apiladas'},
                    {'label': 'Gráfico de Barras Agrupadas', 'value': 'barras_agrupadas'},
                    {'label': 'Gráfico de Columnas Agrupadas', 'value': 'columnas_agrupadas'},
                    {'label': 'Gráfico de Líneas', 'value': 'lineas'},
                    {'label': 'Gráfico de Cintas', 'value': 'cintas'},
                    {'label': 'Gráfico Circular', 'value': 'circular'},
                    {'label': 'Gráfico de Anillos', 'value': 'anillos'},
                    {'label': 'Gráfico de Área', 'value': 'area'}
                ],
                placeholder='Selecciona un tipo de gráfico',
                style={'margin-bottom': '10px'}
            ),
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='descripcion-imagen1', 
                config={'displayModeBar': False},
                style={'display': 'flex', 'justify-content': 'center',  'align-items': 'center',  'height': '20vh'}
            ),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-chart1'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P(id='suma-cantidad-label1', style={'font-weight': 'bold'}),
            html.P(id='precio-unitario-maximo-label1', style={'font-weight': 'bold'})
        ], width=5),
        dbc.Col([
            html.Button('Exportar a PDF', id='export-pdf-button1', n_clicks=0)
        ]),
        dbc.Col([
            dbc.Label("Rango de Fechas"),
            dcc.DatePickerRange(
                id='date-picker-range1',
                min_date_allowed=df['fecha_ingreso'].min().date(),
                max_date_allowed=df['fecha_ingreso'].max().date(),
                start_date=df['fecha_ingreso'].min().date(),
                end_date=df['fecha_ingreso'].max().date(),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '10px'}
            ),
        ], width=5),
        dcc.Download(id='download-pdf1')    
    ]),
], fluid=True)

# Crear gráfico inicial sin filtro
fig = px.line(df, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)

# Callback para actualizar el gráfico y las etiquetas según las selecciones
@callback(
    [
        Output('line-chart1', 'figure'),
        Output('suma-cantidad-label1', 'children'),
        Output('precio-unitario-maximo-label1', 'children')
    ],
    [
        Input('codigo-item-dropdown1', 'value'),
        Input('descripcion-dropdown1', 'value'),
        Input('date-picker-range1', 'start_date'),
        Input('date-picker-range1', 'end_date'),
        Input('anio-dropdown1', 'value'),
        Input('tipo-grafico-dropdown1', 'value')  # Nuevo input para el tipo de gráfico
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
        # Gráfico por defecto (si no se selecciona tipo)
        fig = px.line(df_filtrado, x='fecha_ingreso', y='cantidad', title='Cantidad por fecha de ingreso', markers=True)
        
    # Sumar la cantidad total y calcular el precio unitario máximo
    suma_cantidad = df_filtrado['cantidad'].sum()
    precio_unitario_maximo = df_filtrado['precio_unitario'].max()
    
    return fig, f"Suma de Cantidad: {suma_cantidad}", f"Precio Unitario Máximo: {precio_unitario_maximo}"

# Callback para generar la imagen con el texto
@callback(
    Output('descripcion-imagen1', 'figure'),
    [Input('codigo-item-dropdown1', 'value'),
     Input('descripcion-dropdown1', 'value')]
)
def generate_image(codigo_item, descripcion):
    # Inicializar el DataFrame filtrado
    df_filtrado = df.copy()

    # Filtrar el DataFrame según el código de ítem seleccionado
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    
    # Filtrar el DataFrame según la descripción seleccionada (si no hay código de ítem)
    elif descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]

    # Verificar si hay datos después de filtrar
    if not df_filtrado.empty:
        codigo_item = df_filtrado['codigo_item'].iloc[0]
        descripcion_value = df_filtrado['descripcion'].iloc[0]
        codigo_partida = df_filtrado['codigo_partida'].iloc[0]
        partida_presupuestaria = df_filtrado['partida_presupuestaria'].iloc[0]
    else:
        codigo_item = 'Descripción no encontrada'
        descripcion_value = 'Descripción no encontrada'
        codigo_partida = 'Código de partida no encontrado'
        partida_presupuestaria = 'Partida presupuestaria no encontrada'

    # Crear la imagen con el texto utilizando Plotly
    fig = go.Figure()

    fig.add_annotation(
        text=f"Código de Item: {codigo_item}<br>Descripción: {descripcion_value}<br>Código de Partida: {codigo_partida}<br>Partida Presupuestaria: {partida_presupuestaria}",
        xref="paper", yref="paper",
        font=dict(size=20),
        showarrow=False,
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle'
    )

    fig.update_layout(
        title="Información del Código de Ítem",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente para el gráfico
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo transparente para la trama
    )

    return fig

@callback(
    Output('download-pdf1', 'data'),
    [Input('export-pdf-button1', 'n_clicks')],
    [State('line-chart1', 'figure')]
)
def export_to_pdf(n_clicks, fig):
    if n_clicks > 0:
        if fig:
            # Convertir el gráfico a PDF
            buffer = io.BytesIO()
            pio.write_image(fig, buffer, format='pdf')
            buffer.seek(0)
            return dcc.send_bytes(buffer.getvalue(), 'grafico.pdf')
    return None

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)