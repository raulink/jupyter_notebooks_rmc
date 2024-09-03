import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import io
import plotly.io as pio
from dotenv import load_dotenv
import plotly.graph_objects as go

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conéctate a la base de datos MySQL
engine = create_engine('mysql+pymysql://mantto:Sistemas0,@192.168.100.50/Catalogo')

# Cargar datos desde la tabla 'salida' a un DataFrame
df = pd.read_sql('SELECT * FROM salida;', engine)

# Convertir la columna 'fecha_salida' a tipo de datos datetime
df['fecha_salida'] = pd.to_datetime(df['fecha_salida'], dayfirst=True)

# Reemplazar `None` o `null` por un valor adecuado en las columnas problemáticas
df['clasificacion_trabajo'] = df['clasificacion_trabajo'].fillna('')
df['partida_presupuestaria'] = df['partida_presupuestaria'].fillna('')
df['ubicacion'] = df['ubicacion'].fillna('')

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Crear el layout de la aplicación
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Label("Código de Item"),
                dcc.Dropdown(
                    id='codigo-item-dropdown2',
                    options=[{'label': str(item), 'value': item} for item in df['codigo_item'].unique()],
                    placeholder='Selecciona un código de item',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Label("Descripción"),
                dcc.Dropdown(
                    id='descripcion-dropdown2',
                    options=[{'label': str(desc), 'value': desc} for desc in df['descripcion'].unique()],
                    placeholder='Selecciona una descripción',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Label("Clasificación de Trabajo"),
                dcc.Dropdown(
                    id='clasificacion-trabajo-dropdown2',
                    options=[{'label': str(clas), 'value': clas} for clas in df['clasificacion_trabajo'].unique()],
                    placeholder='Selecciona una clasificación de trabajo',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Label("Año"),
                dcc.Dropdown(
                    id='anio-dropdown2',
                    options=[{'label': str(anio), 'value': str(anio)} for anio in df['fecha_salida'].dt.year.unique()],
                    placeholder='Selecciona un año',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Label("Partida Presupuestaria"),
                dcc.Dropdown(
                    id='partida-presupuestaria-dropdown2',
                    options=[{'label': str(partida), 'value': partida} for partida in df['partida_presupuestaria'].unique()],
                    placeholder='Selecciona una partida presupuestaria',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Label("Tipo de Gráfico"),
                dcc.Dropdown(
                    id='tipo-grafico-dropdown2',
                    options=[
                        {'label': 'Gráfico de barras apiladas', 'value': 'bar_stack'},
                        {'label': 'Gráfico de columnas apiladas', 'value': 'bar_stack_col'},
                        {'label': 'Gráfico de barras agrupadas', 'value': 'bar_group'},
                        {'label': 'Gráfico de columnas agrupadas', 'value': 'bar_group_col'},
                        {'label': 'Gráfico de líneas', 'value': 'line'},
                        {'label': 'Gráfico de cintas', 'value': 'funnel'},
                        {'label': 'Gráfico circular', 'value': 'pie'},
                        {'label': 'Gráfico de anillos', 'value': 'donut'},
                        {'label': 'Gráfico de área', 'value': 'area'}
                    ],
                    placeholder='Selecciona un tipo de gráfico',
                    style={'margin-bottom': '7px'}
                ),
            ], width=2),  
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='descripcion-imagen2', 
                    config={'displayModeBar': False},
                    style={'display': 'flex', 'justify-content': 'center',  'align-items': 'center',  'height': '20vh'}
                ),
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='line-chart2'),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.P(id='suma-cantidad-label2', style={'font-weight': 'bold'}),
                html.P(id='precio-unitario-maximo-label2', style={'font-weight': 'bold'}),
            ]),
            dbc.Col([
                html.Button('Exportar a PDF', id='export-pdf-button2', n_clicks=0)
                ]),
            dbc.Col([
                dbc.Label("Rango de Fechas"),
                dcc.DatePickerRange(
                    id='date-picker-range2',
                    min_date_allowed=df['fecha_salida'].min().date(),
                    max_date_allowed=df['fecha_salida'].max().date(),
                    start_date=df['fecha_salida'].min().date(),
                    end_date=df['fecha_salida'].max().date(),
                    display_format='YYYY-MM-DD',
                    style={'margin-bottom': '10px'}
                ),
            ], width=6),
        ]),
        dcc.Download(id='download-pdf2')
    ], fluid=True),
])

# Crear gráfico inicial sin filtro
fig = px.line(df, x='fecha_salida', y='cantidad', title='Cantidad por fecha de salida', markers=True)

# Callback para actualizar el gráfico y las etiquetas según los valores seleccionados en los comboboxes y el datepicker range
@callback(
    [
        Output('line-chart2', 'figure'),
        Output('suma-cantidad-label2', 'children'),
        Output('precio-unitario-maximo-label2', 'children')
    ],
    [
        Input('codigo-item-dropdown2', 'value'),
        Input('descripcion-dropdown2', 'value'),
        Input('date-picker-range2', 'start_date'),
        Input('date-picker-range2', 'end_date'),
        Input('clasificacion-trabajo-dropdown2', 'value'),
        Input('partida-presupuestaria-dropdown2', 'value'),
        Input('tipo-grafico-dropdown2', 'value')
    ]
)
def update_graph_and_labels(codigo_item, descripcion, start_date, end_date, clasificacion_trabajo, partida_presupuestaria, tipo_grafico):
    # Filtrar datos según los valores seleccionados en los comboboxes y el rango de fechas
    df_filtrado = df.copy()

    # Filtrar datos según los valores seleccionados
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    if descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]
    if start_date and end_date:
        df_filtrado = df_filtrado[(df_filtrado['fecha_salida'] >= start_date) & (df_filtrado['fecha_salida'] <= end_date)]
    if clasificacion_trabajo:
        df_filtrado = df_filtrado[df_filtrado['clasificacion_trabajo'] == clasificacion_trabajo]
    if partida_presupuestaria:
        df_filtrado = df_filtrado[df_filtrado['partida_presupuestaria'] == partida_presupuestaria]

    # Agrupar datos por fecha, ubicación, y sumar la cantidad
    df_agrupado = df_filtrado.groupby([df_filtrado['fecha_salida'].dt.to_period('M'), 'ubicacion'])['cantidad'].sum().reset_index()
    df_agrupado['fecha_salida'] = df_agrupado['fecha_salida'].astype(str)

    # Crear gráfico según el tipo seleccionado
    if tipo_grafico == 'bar_stack':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida', text='cantidad', labels={'cantidad': 'Cantidad'})
    elif tipo_grafico == 'bar_stack_col':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida', text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='stack')
    elif tipo_grafico == 'bar_group':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida', text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='group')
    elif tipo_grafico == 'bar_group_col':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida', text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='group')
    elif tipo_grafico == 'line':
        fig = px.line(df_agrupado, x='fecha_salida', y='cantidad', title='Cantidad por fecha de salida', color='ubicacion', markers=True)
    elif tipo_grafico == 'funnel':
        fig = px.funnel(df_agrupado, x='fecha_salida', y='cantidad', title='Cantidad por fecha de salida', color='ubicacion')
    elif tipo_grafico == 'pie':
        fig = px.pie(df_agrupado, names='ubicacion', values='cantidad', title='Cantidad por ubicación')
    elif tipo_grafico == 'donut':
        fig = px.pie(df_agrupado, names='ubicacion', values='cantidad', title='Cantidad por ubicación', hole=0.4)
    elif tipo_grafico == 'area':
        fig = px.area(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida')
    else:
        # Default to line chart if no type selected
        fig = px.area(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title='Cantidad por fecha de salida')

    fig.update_layout(height=600)

    # Calcular la suma de cantidades
    suma_cantidad = df_filtrado['cantidad'].sum()
    
    # Calcular el precio unitario máximo
    precio_unitario_maximo = df_filtrado['precio_unitario'].max()
    
    # Formatear los resultados como cadenas de texto para mostrarlos en las etiquetas
    suma_cantidad_label = f"Suma de cantidades: {suma_cantidad}"
    precio_unitario_maximo_label = f"Precio unitario máximo: {precio_unitario_maximo}"

    return fig, suma_cantidad_label, precio_unitario_maximo_label

# Callback para generar la imagen con el texto
@callback(
    Output('descripcion-imagen2', 'figure'),
    [Input('codigo-item-dropdown2', 'value'),
     Input('descripcion-dropdown2', 'value')]
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
    Output('download-pdf2', 'data'),
    [Input('export-pdf-button2', 'n_clicks')],
    [State('line-chart2', 'figure')]
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
