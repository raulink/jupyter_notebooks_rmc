import os
import io
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# --- Configuración de Base de Datos ---
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

# --- Aplicación Dash ---
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # Encabezado
    dbc.Row([
        dbc.Col(html.H2("Panel de Control de Salidas", className="text-center my-4"), width=12)
    ]),

    # Sección de Filtros Superiores
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Código de Item"),
                    dcc.Dropdown(
                        id='codigo-item-dropdown2',
                        options=[{'label': str(item), 'value': item} for item in df['codigo_item'].unique()],
                        placeholder='Selecciona código',
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),
                dbc.Col([
                    dbc.Label("Descripción"),
                    dcc.Dropdown(
                        id='descripcion-dropdown2',
                        options=[{'label': str(desc), 'value': desc} for desc in df['descripcion'].unique()],
                        placeholder='Selecciona descripción',
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),
                dbc.Col([
                    dbc.Label("Clasificación de Trabajo"),
                    dcc.Dropdown(
                        id='clasificacion-trabajo-dropdown2',
                        options=[{'label': str(clas), 'value': clas} for clas in df['clasificacion_trabajo'].unique() if clas != ''],
                        placeholder='Clasificación',
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),
                dbc.Col([
                    dbc.Label("Año"),
                    dcc.Dropdown(
                        id='anio-dropdown2',
                        options=[{'label': str(anio), 'value': str(anio)} for anio in df['fecha_salida'].dt.year.unique()],
                        placeholder='Selecciona año',
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),
                dbc.Col([
                    dbc.Label("Partida Presupuestaria"),
                    dcc.Dropdown(
                        id='partida-presupuestaria-dropdown2',
                        options=[{'label': str(partida), 'value': partida} for partida in df['partida_presupuestaria'].unique() if partida != ''],
                        placeholder='Partida',
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),
                dbc.Col([
                    dbc.Label("Tipo de Gráfico"),
                    dcc.Dropdown(
                        id='tipo-grafico-dropdown2',
                        options=[
                            {'label': 'Barras Apiladas', 'value': 'bar_stack'},
                            {'label': 'Columnas Apiladas', 'value': 'bar_stack_col'},
                            {'label': 'Barras Agrupadas', 'value': 'bar_group'},
                            {'label': 'Columnas Agrupadas', 'value': 'bar_group_col'},
                            {'label': 'Líneas', 'value': 'line'},
                            {'label': 'Cintas (Funnel)', 'value': 'funnel'},
                            {'label': 'Circular', 'value': 'pie'},
                            {'label': 'Anillos', 'value': 'donut'},
                            {'label': 'Área', 'value': 'area'}
                        ],
                        placeholder='Tipo de gráfico',
                        value='area', # Valor por defecto
                        className="mb-3"
                    ),
                ], xs=12, md=4, lg=2),  
            ]),
        ])
    ], className="mb-4 shadow-sm"),

    # Sección de Información Detallada
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Detalles del Ítem Seleccionado"),
                dbc.CardBody([
                    dcc.Graph(
                        id='descripcion-imagen2', 
                        config={'displayModeBar': False},
                        style={'height': '150px'}
                    ),
                ])
            ], className="mb-4 shadow-sm")
        ], width=12),
    ]),

    # Gráfico Principal
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart2'),
                ])
            ], className="mb-4 shadow-sm")
        ]),
    ]),

    # Footer con Resumen, Rango de Fechas y Exportación
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("Resumen de Datos", className="card-title"),
                    dbc.Alert([
                        html.Div(id='suma-cantidad-label2'),
                        html.Div(id='precio-unitario-maximo-label2'),
                    ], color="success"), # Color verde para distinguir de ingresos
                ], xs=12, md=4),
                
                dbc.Col([
                    dbc.Label("Rango de Fechas de Salida"),
                    html.Br(),
                    dcc.DatePickerRange(
                        id='date-picker-range2',
                        min_date_allowed=df['fecha_salida'].min().date(),
                        max_date_allowed=df['fecha_salida'].max().date(),
                        start_date=df['fecha_salida'].min().date(),
                        end_date=df['fecha_salida'].max().date(),
                        display_format='YYYY-MM-DD',
                        style={'border': '1px solid #ccc', 'borderRadius': '4px', 'width': '100%'}
                    ),
                ], xs=12, md=5),

                dbc.Col([
                    dbc.Label("Acciones"),
                    html.Br(),
                    dbc.Button(
                        'Exportar a PDF', 
                        id='export-pdf-button2', 
                        color="danger", 
                        className="w-100 mt-1",
                        n_clicks=0
                    ),
                    dcc.Download(id='download-pdf2')
                ], xs=12, md=3),
            ], align="center"),
        ])
    ], className="mb-5 shadow-sm"),

], fluid=True, style={'backgroundColor': '#f8f9fa'})

# --- Callbacks ---

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
        Input('tipo-grafico-dropdown2', 'value'),
        Input('anio-dropdown2', 'value')
    ]
)
def update_graph_and_labels(codigo_item, descripcion, start_date, end_date, clasificacion_trabajo, partida_presupuestaria, tipo_grafico, anio):
    df_filtrado = df.copy()

    # Aplicar filtros
    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    if descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]
    if start_date and end_date:
        df_filtrado = df_filtrado[(df_filtrado['fecha_salida'] >= start_date) & (df_filtrado['fecha_salida'] <= end_date)]
    if anio:
        df_filtrado = df_filtrado[df_filtrado['fecha_salida'].dt.year == int(anio)]
    if clasificacion_trabajo:
        df_filtrado = df_filtrado[df_filtrado['clasificacion_trabajo'] == clasificacion_trabajo]
    if partida_presupuestaria:
        df_filtrado = df_filtrado[df_filtrado['partida_presupuestaria'] == partida_presupuestaria]

    # Agrupar datos por fecha (mes), ubicación, y sumar la cantidad
    df_agrupado = df_filtrado.groupby([df_filtrado['fecha_salida'].dt.to_period('M'), 'ubicacion'])['cantidad'].sum().reset_index()
    df_agrupado['fecha_salida'] = df_agrupado['fecha_salida'].astype(str)

    title_text = 'Cantidad por fecha de salida'
    
    # Crear gráfico según el tipo seleccionado
    if tipo_grafico == 'bar_stack':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text, text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='stack')
    elif tipo_grafico == 'bar_stack_col':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text, text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='stack')
    elif tipo_grafico == 'bar_group':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text, text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='group')
    elif tipo_grafico == 'bar_group_col':
        fig = px.bar(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text, text='cantidad', labels={'cantidad': 'Cantidad'}, barmode='group')
    elif tipo_grafico == 'line':
        fig = px.line(df_agrupado, x='fecha_salida', y='cantidad', title=title_text, color='ubicacion', markers=True)
    elif tipo_grafico == 'funnel':
        fig = px.funnel(df_agrupado, x='fecha_salida', y='cantidad', title=title_text, color='ubicacion')
    elif tipo_grafico == 'pie':
        fig = px.pie(df_agrupado, names='ubicacion', values='cantidad', title='Cantidad por ubicación')
    elif tipo_grafico == 'donut':
        fig = px.pie(df_agrupado, names='ubicacion', values='cantidad', title='Cantidad por ubicación', hole=0.4)
    elif tipo_grafico == 'area':
        fig = px.area(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text)
    else:
        fig = px.area(df_agrupado, x='fecha_salida', y='cantidad', color='ubicacion', title=title_text)

    fig.update_layout(template='plotly_white', margin=dict(t=50, b=20, l=20, r=20), height=500)

    # Calcular resúmenes
    suma_cantidad = df_filtrado['cantidad'].sum()
    precio_unitario_maximo = df_filtrado['precio_unitario'].max() if not df_filtrado.empty else 0
    
    suma_cantidad_label = f"Suma Total de Cantidades: {suma_cantidad}"
    precio_unitario_maximo_label = f"Precio Unitario Máximo: ${precio_unitario_maximo:,.2f}"

    return fig, suma_cantidad_label, precio_unitario_maximo_label


@callback(
    Output('descripcion-imagen2', 'figure'),
    [Input('codigo-item-dropdown2', 'value'),
     Input('descripcion-dropdown2', 'value')]
)
def generate_image(codigo_item, descripcion):
    df_filtrado = df.copy()

    if codigo_item:
        df_filtrado = df_filtrado[df_filtrado['codigo_item'] == codigo_item]
    elif descripcion:
        df_filtrado = df_filtrado[df_filtrado['descripcion'] == descripcion]

    if not df_filtrado.empty:
        item = df_filtrado.iloc[0]
        text_content = (f"<b>Código:</b> {item['codigo_item']} | <b>Descripción:</b> {item['descripcion']}<br>"
                        f"<b>Partida:</b> {item.get('codigo_partida', 'N/A')} - {item.get('partida_presupuestaria', 'N/A')}")
    else:
        text_content = "Seleccione un ítem para ver los detalles"

    fig = go.Figure()
    fig.add_annotation(
        text=text_content,
        xref="paper", yref="paper",
        font=dict(size=16),
        showarrow=False, x=0.5, y=0.5
    )
    
    fig.update_layout(
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


@callback(
    Output('download-pdf2', 'data'),
    [Input('export-pdf-button2', 'n_clicks')],
    [State('line-chart2', 'figure')],
    prevent_initial_call=True
)
def export_to_pdf(n_clicks, fig):
    if n_clicks > 0 and fig:
        buffer = io.BytesIO()
        pio.write_image(fig, buffer, format='pdf')
        buffer.seek(0)
        return dcc.send_bytes(buffer.getvalue(), 'grafico_salidas.pdf')
    return None

if __name__ == '__main__':
    app.run(debug=True, port=8051)