import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from datetime import datetime, timedelta
import dash

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conéctate a la base de datos MySQL con manejo de errores
try:
    engine = create_engine('mysql+pymysql://zona1:Sistemas0.@192.168.100.60/opmt2')
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Cargar datos de una sola vez y procesar en pandas
try:
    df_operativos = pd.read_sql('SELECT * FROM datosoperativos;', engine)
    lineas = df_operativos['linea'].unique()
    secciones = df_operativos['seccion'].unique()
except Exception as e:
    print(f"Error al cargar los datos: {e}")

# Definir el mapeo de rangos de tiempo globalmente
time_mapping = {
    'Últimos 5 minutos': timedelta(minutes=5),
    'Últimos 15 minutos': timedelta(minutes=15),
    'Últimos 30 minutos': timedelta(minutes=30),
    'Última 1 hora': timedelta(hours=1),
    'Últimas 3 horas': timedelta(hours=3),
    'Últimas 6 horas': timedelta(hours=6),
    'Últimas 12 horas': timedelta(hours=12),
    'Últimas 24 horas': timedelta(hours=24),
    'Últimos 2 días': timedelta(days=2),
    'Últimos 7 días': timedelta(days=7),
    'Últimos 30 días': timedelta(days=30),
    'Últimos 90 días': timedelta(days=90),
    'Últimos 6 meses': timedelta(days=180),
    'Último 1 año': timedelta(days=365),
    'Últimos 2 años': timedelta(days=730),
    'Últimos 5 años': timedelta(days=1825),
}

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Función para calcular las fechas según la selección del rango de tiempo
def calculate_date_range(time_range):
    end_date = datetime.now()
    start_date = end_date - time_mapping.get(time_range, timedelta(days=30))  # Valor por defecto: 30 días
    return start_date, end_date

# Consultas para los graficos de Boton Horometro
def query_horometro_motor(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
           CAST(hrs1acc AS DECIMAL(10,2)) AS value1,
           CAST(hrs2acc AS DECIMAL(10,2)) AS value2
    FROM datosoperativos
    WHERE hrs1acc <> '' AND hrs2acc <> ''
      AND linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

def query_horometro(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
           CAST(hrshmi AS DECIMAL(10,2)) AS value
    FROM datosoperativos
    WHERE hrshmi <> ''
      AND linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

def query_horometros_motor(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
           CAST(hrs1acc AS DECIMAL(10,2)) AS Motor1,
           CAST(hrs2acc AS DECIMAL(10,2)) AS Motor2
    FROM datosoperativos
    WHERE hrs1acc <> ''
      AND linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Consultas para los graficos de Boton Pruebas de frenado

# Distancia frenado (m)
def query_distancia_frenado(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(dfspf AS DECIMAL(10,2)) AS StopFS,
        CAST(dfepf AS DECIMAL(10,2)) AS StopFE,
        CAST(dspf AS DECIMAL(10,2)) AS Stop,
        CAST(dempf AS DECIMAL(10,2)) AS Emergencia
    FROM datosoperativos
    WHERE linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s
      AND dfspf <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Tiempo frenado (s)
def query_tiempo_frenado(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(tfspf AS DECIMAL(10,2)) AS StopFS,
        CAST(tfepf AS DECIMAL(10,2)) AS StopFE,
        CAST(tspf AS DECIMAL(10,2)) AS Stop,
        CAST(tempf AS DECIMAL(10,2)) AS Emergencia
    FROM datosoperativos
    WHERE linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s
      AND tfspf <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Desaceleración frenado (m/s2) Query 1
def query_desaceleracion_frenado1(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(decfspf AS DECIMAL(10,2)) AS StopFS,
        CAST(decfepf AS DECIMAL(10,2)) AS StopFE
    FROM datosoperativos
    WHERE linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s
      AND decfspf <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Desaceleración frenado (m/s2) Query 2
def query_desaceleracion_frenado2(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(decspf AS DECIMAL(10,2)) AS Stop,
        CAST(decempf AS DECIMAL(10,2)) AS Emergencia
    FROM datosoperativos
    WHERE linea = %s
      AND seccion = %s
      AND fecha BETWEEN %s AND %s
      AND decspf <> '-'
      AND decempf <> '-';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Consultas para los graficos de Boton Generadores

# Horómetros Generadores ======QUERY 1=======
def query_horometros_generadores1(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(hrsmt AS DECIMAL(10,2)) AS MotTermico,
        CAST(hrsga AS DECIMAL(10,2)) AS GenAux1
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Horómetros Generadores ======QUERY 2=======
def query_horometros_generadores2(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(hrsga2 AS DECIMAL(10,2)) AS GenAux2
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND hrsga2 <>'';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Horómetros Generadores ======QUERY 3=======
def query_horometros_generadores3(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(hrsgr AS DECIMAL(10,2)) AS GenRecuperacion
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND hrsgr <>'';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Combustible(%) ======QUERY 1=======
def query_combustible1(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(ncmt AS DECIMAL(10,2)) AS MotorTermico
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND ncmt <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Combustible(%) ======QUERY 2=======
def query_combustible2(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(ncga AS DECIMAL(10,2)) AS GenAuxiliar1
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND ncga <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Combustible(%) ======QUERY 3=======
def query_combustible3(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(ncga2 AS DECIMAL(10,2)) AS GenAuxiliar2
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND ncga2 <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Combustible(%) ======QUERY 4=======
def query_combustible4(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(ncgr AS DECIMAL(10,2)) AS GenRecuperacion
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND ncgr <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df


# Consultas para los graficos de Boton Dispositivos de Control

# Partidas por año
def query_partidas_anio(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        CAST(parthmi AS DECIMAL(10,0)) AS PartidasAnio
    FROM datosoperativos
    WHERE linea = %s 
        AND seccion = %s
        AND fecha BETWEEN %s AND %s
        AND parthmi <> '';
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Recorrido del Cable (Km)
def query_recorrido_cable(linea, seccion, start_date, end_date):
    query = """
    select fecha, 
        sum(Recorrido) 
    from (
        select fecha, desde, hasta, velocidad as 'VelM/s', 
        TIMEDIFF(hasta,desde)*0.3600 as Delta, 
        ((TIMEDIFF(hasta,desde)*0.3600)*velocidad) as Recorrido 
        from velocidades 
        where linea = %s
            and (modo = 'S12' or modo = 'S1' or modo = 'S2') 
        ORDER BY FECHA 
    )data 
    GROUP BY fecha;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

# Horas de Funcionamiento por dia (H)
def query_horas_funcionamiento(linea, seccion, start_date, end_date):
    query = """
    SELECT fecha,
        MAX(foc) - MAX(ioc) AS horas
    FROM datosoperativos 
    WHERE linea = %s
        AND (ioc != '' OR foc != '')
    GROUP BY fecha, linea
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection, params=(linea, seccion, start_date, end_date))
    return df

STYLE_CENTER = {'textAlign': 'center'}

# Layout de la aplicación con dropdowns y botones mejorados
layout = html.Div([
    dbc.Container([
        
        html.H1('Dashboard Operaciones', style=STYLE_CENTER),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='linea-dropdown3',
                    options=[{'label': linea, 'value': linea} for linea in lineas],
                    placeholder="Selecciona una Línea"
                ),
            ], width=2),
            dbc.Col([
                dcc.Dropdown(
                    id='seccion-dropdown3',
                    options=[{'label': seccion, 'value': seccion} for seccion in secciones],
                    placeholder="Selecciona una Sección"
                ),
            ], width=2),
            dbc.Col([
                dcc.Dropdown(
                    id='time-range-dropdown3',
                    options=[
                        {'label': label, 'value': label} for label in time_mapping.keys()
                    ],
                    placeholder="Selecciona un Rango de Tiempo"
                ),
            ], width=2),
            dbc.Col([
                dcc.DatePickerRange(
                    id='date-picker-range3',
                    start_date_placeholder_text="Fecha de inicio",
                    end_date_placeholder_text="Fecha de fin",
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('Horometro', id='toggle-button1', n_clicks=0, color="primary", className="me-2"),
                        dbc.Button(html.I(className="fas fa-edit"), id='edit-button1', color="warning", className="me-2"),
                        dbc.Button(html.I(className="fas fa-trash"), id='delete-button1', color="danger"),
                    ]),
                ]),
                dbc.Collapse(
                    dcc.Graph(id='Hour-meter-chart1'),
                    id='collapse1',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='Hour-meter-chart2'),
                    id='collapse2',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='Hour-meter-chart3'),
                    id='collapse3',
                    is_open=False
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('Pruebas de Frenado', id='toggle-button2', n_clicks=0, color="primary", className="me-2"),
                        dbc.Button(html.I(className="fas fa-edit"), id='edit-button2', color="warning", className="me-2"),
                        dbc.Button(html.I(className="fas fa-trash"), id='delete-button2', color="danger"),
                    ]),
                ]),
                dbc.Collapse(
                    dcc.Graph(id='braking-tests-chart1'),
                    id='collapse4',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='braking-tests-chart2'),
                    id='collapse5',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='braking-tests-chart3'),
                    id='collapse6',
                    is_open=False
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('Generadores', id='toggle-button3', n_clicks=0, color="primary", className="me-2"),
                        dbc.Button(html.I(className="fas fa-edit"), id='edit-button3', color="warning", className="me-2"),
                        dbc.Button(html.I(className="fas fa-trash"), id='delete-button3', color="danger"),
                    ]),
                ]),
                dbc.Collapse(
                    dcc.Graph(id='generators-chart1'),
                    id='collapse7',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='generators-chart2'),
                    id='collapse8',
                    is_open=False
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('Dispositivos de Control', id='toggle-button4', n_clicks=0, color="primary", className="me-2"),
                        dbc.Button(html.I(className="fas fa-edit"), id='edit-button4', color="warning", className="me-2"),
                        dbc.Button(html.I(className="fas fa-trash"), id='delete-button4', color="danger"),
                    ]),
                ]),
                dbc.Collapse(
                    dcc.Graph(id='control-devices-chart1'),
                    id='collapse9',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='control-devices-chart2'),
                    id='collapse10',
                    is_open=False
                ),
                dbc.Collapse(
                    dcc.Graph(id='control-devices-chart3'),
                    id='collapse11',
                    is_open=False
                ),
            ]),
        ]),
    ], fluid=True),
])

# Callback optimizado con patrones de MATCH y ALL
@callback(
    [Output(f'collapse{i}', 'is_open') for i in range(1, 12)],
    [Input('toggle-button1', 'n_clicks'),
     Input('toggle-button2', 'n_clicks'),
     Input('toggle-button3', 'n_clicks'),
     Input('toggle-button4', 'n_clicks')],
    [State(f'collapse{i}', 'is_open') for i in range(1, 12)]
)
def toggle_collapse(btn1, btn2, btn3, btn4, *is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    toggle_state = list(is_open)

    toggle_map = {
        'toggle-button1': (0, 1, 2),
        'toggle-button2': (3, 4, 5),
        'toggle-button3': (6, 7),
        'toggle-button4': (8, 9, 10)
    }

    for idx in toggle_map.get(button_id, []):
        toggle_state[idx] = not toggle_state[idx]

    return toggle_state

# Callback para actualizar los tres gráficos
@callback(
    [Output('Hour-meter-chart1', 'figure'),
     Output('Hour-meter-chart2', 'figure'),
     Output('Hour-meter-chart3', 'figure')],
    [Input('linea-dropdown3', 'value'),
     Input('seccion-dropdown3', 'value'),
     Input('time-range-dropdown3', 'value'),
     Input('date-picker-range3', 'start_date'),
     Input('date-picker-range3', 'end_date')],
    prevent_initial_call=True
)
def update_all_charts(linea, seccion, time_range, start_date, end_date):
    if not linea or not seccion:
        return dash.no_update, dash.no_update, dash.no_update

    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)

    # Actualizar gráfico 1 (query_horometro_motor)
    df_motor = query_horometro_motor(linea, seccion, start_date, end_date)
    if df_motor.empty:
        figure1 = dash.no_update
    else:
        figure1 = {
            'data': [
                {'x': df_motor['fecha'], 'y': df_motor['value1'], 'type': 'line', 'name': 'Motor 1'},
                {'x': df_motor['fecha'], 'y': df_motor['value2'], 'type': 'line', 'name': 'Motor 2'}
            ],
            'layout': {
                'title': f'Horómetro Motor para Línea {linea} y Sección {seccion}',
                'xaxis': {'title': 'Fecha'},
                'yaxis': {'title': 'Horas'}
            }
        }

    # Actualizar gráfico 2 (query_horometro)
    df_horometro = query_horometro(linea, seccion, start_date, end_date)
    if df_horometro.empty:
        figure2 = dash.no_update
    else:
        figure2 = {
            'data': [
                {'x': df_horometro['fecha'], 'y': df_horometro['value'], 'type': 'line', 'name': 'Horometro'}
            ],
            'layout': {
                'title': f'Horómetro para Línea {linea} y Sección {seccion}',
                'xaxis': {'title': 'Fecha'},
                'yaxis': {'title': 'Horas'}
            }
        }

    # Actualizar gráfico 3 (query_horometros_motor)
    df_horometros = query_horometros_motor(linea, seccion, start_date, end_date)
    if df_horometros.empty:
        figure3 = dash.no_update
    else:
        figure3 = {
            'data': [
                {'x': df_horometros['fecha'], 'y': df_horometros['Motor1'], 'type': 'line', 'name': 'Motor 1'},
                {'x': df_horometros['fecha'], 'y': df_horometros['Motor2'], 'type': 'line', 'name': 'Motor 2'}
            ],
            'layout': {
                'title': f'Horómetros Motor 1 y Motor 2 para Línea {linea} y Sección {seccion}',
                'xaxis': {'title': 'Fecha'},
                'yaxis': {'title': 'Horas'}
            }
        }

    return figure1, figure2, figure3

# Callback para actualizar los tres gráficos
@callback(
    [Output('braking-tests-chart1', 'figure'),
     Output('braking-tests-chart2', 'figure'),
     Output('braking-tests-chart3', 'figure')],
    [Input('linea-dropdown3', 'value'),
     Input('seccion-dropdown3', 'value'),
     Input('time-range-dropdown3', 'value')],
)
def update_braking_tests(linea, seccion, time_range):
    if not linea or not seccion or not time_range:
        return {}, {}, {}

    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)

    # Obtener datos
    df_distancia = query_distancia_frenado(linea, seccion, start_date, end_date)
    df_tiempo = query_tiempo_frenado(linea, seccion, start_date, end_date)
    df_desaceleracion1 = query_desaceleracion_frenado1(linea, seccion, start_date, end_date)
    df_desaceleracion2 = query_desaceleracion_frenado2(linea, seccion, start_date, end_date)

    # Crear gráficos (puedes usar plotly.express o go.Figure según prefieras)
    fig_distancia = {
        'data': [{'x': df_distancia['fecha'], 'y': df_distancia['StopFS'], 'type': 'line', 'name': 'StopFS'},
                 {'x': df_distancia['fecha'], 'y': df_distancia['StopFE'], 'type': 'line', 'name': 'StopFE'},
                 {'x': df_distancia['fecha'], 'y': df_distancia['Stop'], 'type': 'line', 'name': 'Stop'},
                 {'x': df_distancia['fecha'], 'y': df_distancia['Emergencia'], 'type': 'line', 'name': 'Emergencia'}]
    }

    fig_tiempo = {
        'data': [{'x': df_tiempo['fecha'], 'y': df_tiempo['StopFS'], 'type': 'line', 'name': 'StopFS'},
                 {'x': df_tiempo['fecha'], 'y': df_tiempo['StopFE'], 'type': 'line', 'name': 'StopFE'},
                 {'x': df_tiempo['fecha'], 'y': df_tiempo['Stop'], 'type': 'line', 'name': 'Stop'},
                 {'x': df_tiempo['fecha'], 'y': df_tiempo['Emergencia'], 'type': 'line', 'name': 'Emergencia'}]
    }

    fig_desaceleracion = {
        'data': [{'x': df_desaceleracion1['fecha'], 'y': df_desaceleracion1['StopFS'], 'type': 'line', 'name': 'StopFS'},
                 {'x': df_desaceleracion1['fecha'], 'y': df_desaceleracion1['StopFE'], 'type': 'line', 'name': 'StopFE'},
                 {'x': df_desaceleracion2['fecha'], 'y': df_desaceleracion2['Stop'], 'type': 'line', 'name': 'Stop'},
                 {'x': df_desaceleracion2['fecha'], 'y': df_desaceleracion2['Emergencia'], 'type': 'line', 'name': 'Emergencia'}]
    }

    return fig_distancia, fig_tiempo, fig_desaceleracion

@callback(
    Output('generators-chart1', 'figure'),
    [Input('linea-dropdown3', 'value'), 
     Input('seccion-dropdown3', 'value'), 
     Input('time-range-dropdown3', 'value')]
)
def update_horometros_generadores(linea, seccion, time_range):
    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)
    
    # Consultar los datos
    df_generadores1 = query_horometros_generadores1(linea, seccion, start_date, end_date)
    df_generadores2 = query_horometros_generadores2(linea, seccion, start_date, end_date)
    df_generadores3 = query_horometros_generadores3(linea, seccion, start_date, end_date)
    
    # Unir las consultas en un solo DataFrame
    df = pd.merge(pd.merge(df_generadores1, df_generadores2, on='fecha', how='outer'), df_generadores3, on='fecha', how='outer')
    
    # Crear la figura de plotly
    fig_hourmeter_generators = {
        'data': [
            {'x': df['fecha'], 'y': df['MotTermico'], 'type': 'line', 'name': 'MotTermico'},
            {'x': df['fecha'], 'y': df['GenAux1'], 'type': 'line', 'name': 'GenAux1'},
            {'x': df['fecha'], 'y': df['GenAux2'], 'type': 'line', 'name': 'GenAux2'},
            {'x': df['fecha'], 'y': df['GenRecuperacion'], 'type': 'line', 'name': 'GenRecuperacion'}
        ],
        'layout': {
            'title': 'Horómetros Generadores',
            'xaxis': {'title': 'Fecha'},
            'yaxis': {'title': 'Horas'}
        }
    }
    
    return fig_hourmeter_generators

@callback(
    Output('generators-chart2', 'figure'),
    [Input('linea-dropdown3', 'value'), 
     Input('seccion-dropdown3', 'value'), 
     Input('time-range-dropdown3', 'value')]
)
def update_combustible(linea, seccion, time_range):
    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)
    
    # Consultar los datos
    df_combustible1 = query_combustible1(linea, seccion, start_date, end_date)
    df_combustible2 = query_combustible2(linea, seccion, start_date, end_date)
    df_combustible3 = query_combustible3(linea, seccion, start_date, end_date)
    df_combustible4 = query_combustible4(linea, seccion, start_date, end_date)
    
    # Unir las consultas en un solo DataFrame
    df = pd.merge(pd.merge(pd.merge(df_combustible1, df_combustible2, on='fecha', how='outer'), df_combustible3, on='fecha', how='outer'), df_combustible4, on='fecha', how='outer')
    
    # Crear la figura de plotly
    fig_combustible = {
        'data': [
            {'x': df['fecha'], 'y': df['MotorTermico'], 'type': 'line', 'name': 'Motor Térmico'},
            {'x': df['fecha'], 'y': df['GenAuxiliar1'], 'type': 'line', 'name': 'Gen Auxiliar 1'},
            #{'x': df['fecha'], 'y': df['GenAuxiliar2'], 'type': 'line', 'name': 'Gen Auxiliar 2'},
            #{'x': df['fecha'], 'y': df['GenRecuperacion'], 'type': 'line', 'name': 'Gen Recuperación'}
        ],
        'layout': {
            'title': 'Niveles de Combustible',
            'xaxis': {'title': 'Fecha'},
            'yaxis': {'title': 'Porcentaje (%)'}
        }
    }
    return fig_combustible

# Callback para Partidas por Año
@callback(
    Output('control-devices-chart1', 'figure'),
    [Input('linea-dropdown3', 'value'),
     Input('seccion-dropdown3', 'value'),
     Input('time-range-dropdown3', 'value')]
)
def update_partidas_anio(linea, seccion, time_range):
    if not linea or not seccion or not time_range:
        return {}

    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)

    # Consultar datos
    df_partidas = query_partidas_anio(linea, seccion, start_date, end_date)

    # Crear gráfico
    fig_partidas = {
        'data': [{'x': df_partidas['fecha'], 'y': df_partidas['PartidasAnio'], 'type': 'line', 'name': 'Partidas por Año'}],
        'layout': {'title': 'Partidas por Año', 'xaxis': {'title': 'Fecha'}, 'yaxis': {'title': 'Partidas'}}
    }

    return fig_partidas

# Callback para Recorrido del Cable (Km)
@callback(
    Output('control-devices-chart2', 'figure'),
    [Input('linea-dropdown3', 'value'),
     Input('seccion-dropdown3', 'value'),
     Input('time-range-dropdown3', 'value')]
)
def update_recorrido_cable(linea, seccion, time_range):
    if not linea or not seccion or not time_range:
        return {}

    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)

    # Consultar datos
    df_recorrido = query_recorrido_cable(linea, seccion, start_date, end_date)

    # Crear gráfico
    fig_recorrido = {
        'data': [{'x': df_recorrido['fecha'], 'y': df_recorrido['sum(Recorrido)'], 'type': 'line', 'name': 'Recorrido del Cable (Km)'}],
        'layout': {'title': 'Recorrido del Cable (Km)', 'xaxis': {'title': 'Fecha'}, 'yaxis': {'title': 'Kilómetros'}}
    }

    return fig_recorrido

# Callback para Horas de Funcionamiento por Día (H)
@callback(
    Output('control-devices-chart3', 'figure'),
    [Input('linea-dropdown3', 'value'),
     Input('seccion-dropdown3', 'value'),
     Input('time-range-dropdown3', 'value')]
)
def update_horas_funcionamiento(linea, seccion, time_range):
    if not linea or not seccion or not time_range:
        return {}

    # Calcular rango de fechas
    start_date, end_date = calculate_date_range(time_range)

    # Consultar datos
    df_horas = query_horas_funcionamiento(linea, seccion, start_date, end_date)

    # Crear gráfico
    fig_horas = {
        'data': [{'x': df_horas['fecha'], 'y': df_horas['horas'], 'type': 'line', 'name': 'Horas de Funcionamiento por Día'}],
        'layout': {'title': 'Horas de Funcionamiento por Día (H)', 'xaxis': {'title': 'Fecha'}, 'yaxis': {'title': 'Horas'}}
    }

    return fig_horas

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)