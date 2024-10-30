import json
import requests  # Asegúrate de tener instalado requests
import io
import plotly.io as pio
import dash
from dash import dcc, html, Input, Output, State, callback # type: ignore
from dash import dash_table
import plotly.graph_objects as go # type: ignore
import pandas as pd # type: ignore
from datetime import datetime, timedelta

# Constantes para configuraciones de estilos
STYLE_CENTER = {'textAlign': 'center'}
STYLE_INLINE_BLOCK = {'display': 'inline-block', 'verticalAlign': 'top'}
STYLE_TABLE = {'overflowX': 'scroll'}
STYLE_CELL = {'textAlign': 'center'}
STYLE_HEADER = {'fontWeight': 'bold'}

# URL que contiene los datos en formato JSON
URL_JSON = 'https://operaciones.miteleferico.bo/API/total/sistemas/2024-06-01/2024-07-01'

def cargar_datos_json(url):
    try:
        # Realizamos la solicitud GET a la URL
        response = requests.get(url)
        # Comprobamos que la solicitud haya sido exitosa
        response.raise_for_status()
        # Convertimos la respuesta a formato JSON
        datos = response.json()
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos de la URL: {e}")
        return {}

# Cargar los datos desde la URL
datos_json = cargar_datos_json(URL_JSON)

# Diccionario de secciones
SECCIONES = {
    'DISPONIBILIDAD': 'Disponibilidad',
    'CONFIABILIDAD': 'Confiabilidad',
    'TIEMPO MEDIO ENTRE FALLAS (MTBF)': 'MTBF',
    'TIEMPO MEDIO DE RESPUESTA (MTTA)': 'MTTA',
    'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)': 'MTTR'
}


# Nueva función para generar fechas artificiales
def generar_fechas_artificiales(num_datos, start_date='2024-06-01'):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(num_datos)] 

# Función para obtener los datos de una sección específica de una línea
# Modificación en esta función
def obtener_datos_seccion(linea, seccion, start_date=None, end_date=None):
    try:
        secciones = datos_json.get(linea, {})
        if not secciones:
            print(f"No se encontró la línea {linea} en los datos.")
            return pd.DataFrame()

        datos_seccion = []
        num_valores = sum([len(valores) for valores in secciones.values()])  # Total de datos
        fechas_artificiales = generar_fechas_artificiales(num_valores, start_date)  # Generar fechas a partir de start_date

        contador = 0
        for sistema, valores in secciones.items():
            for valor in valores:
                fecha = fechas_artificiales[contador]  # Asignar fecha artificial
                contador += 1
                
                # Convertir a formato datetime para la comparación
                fecha_dt = pd.to_datetime(fecha)

                # Filtrar según el rango de fechas
                if start_date and end_date:
                    if fecha_dt < start_date or fecha_dt > end_date:
                        continue  # Saltar datos fuera del rango
                
                # Añadir los datos filtrados
                datos_seccion.append({
                    'Sistema': sistema,
                    'Valor': valor[seccion],
                    'Fecha': fecha_dt  # Guardar la fecha como datetime
                })

        df_seccion = pd.DataFrame(datos_seccion)
        return df_seccion
    except Exception as e:
        print(f"Error al obtener datos de la sección {seccion} en la línea {linea}: {e}")
        return pd.DataFrame()
# Función para obtener un resumen total de todas las líneas
# Función para obtener los datos de una sección específica de una línea
def obtener_datos_seccion(linea, seccion, start_date=None, end_date=None):
    try:
        secciones = datos_json.get(linea, {})
        if not secciones:
            print(f"No se encontró la línea {linea} en los datos.")
            return pd.DataFrame()

        datos_seccion = []
        num_valores = sum([len(valores) for valores in secciones.values()])  # Total de datos
        fechas_artificiales = generar_fechas_artificiales(num_valores)  # Generar fechas

        contador = 0
        for sistema, valores in secciones.items():
            for valor in valores:
                fecha = fechas_artificiales[contador]  # Asignar fecha artificial
                contador += 1
                # Convertir a formato datetime para la comparación
                fecha_dt = pd.to_datetime(fecha)

                # Filtrar según el rango de fechas
                if start_date and end_date:
                    if fecha_dt < start_date or fecha_dt > end_date:
                        continue  # Saltar datos fuera del rango
                
                # Añadir los datos filtrados
                datos_seccion.append({
                    'Sistema': sistema,
                    'Valor': valor[seccion],
                    'Fecha': fecha_dt  # Guardar la fecha como datetime
                })

        df_seccion = pd.DataFrame(datos_seccion)
        return df_seccion
    except Exception as e:
        print(f"Error al obtener datos de la sección {seccion} en la línea {linea}: {e}")
        return pd.DataFrame()

# Función para obtener el promedio de indicadores de una línea
def obtener_datos_resumen_promedio_linea(linea):
    try:
        sistemas = datos_json.get(linea, {})
        disponibilidad_total = 0
        confiabilidad_total = 0
        mtbf_total = 0
        mtta_total = pd.to_timedelta('00:00:00')
        mttr_total = pd.to_timedelta('00:00:00')
        num_sistemas = len(sistemas)
        
        for sistema, valores in sistemas.items():
            sistema_data = valores[0]  # Accedemos al primer conjunto de valores de cada sistema
            
            # Sumar los valores para cada métrica
            disponibilidad_total += sistema_data.get("Disponibilidad", 0)
            confiabilidad_total += sistema_data.get("Confiabilidad", 0)
            mtbf_total += float(sistema_data.get("MTBF", 0))
            mtta_total += pd.to_timedelta(sistema_data.get("MTTA", "00:00:00"))
            mttr_total += pd.to_timedelta(sistema_data.get("MTTR", "00:00:00"))
        
        # Calcular los promedios finales
        disponibilidad_prom = disponibilidad_total / num_sistemas
        confiabilidad_prom = confiabilidad_total / num_sistemas
        mtbf_prom = mtbf_total / num_sistemas
        mtta_prom = str(mtta_total / num_sistemas)
        mttr_prom = str(mttr_total / num_sistemas)
        
        # Devolver los promedios en formato DataFrame
        resumen = {
            "Disponibilidad": [disponibilidad_prom],
            "Confiabilidad": [confiabilidad_prom],
            "MTBF": [mtbf_prom],
            "MTTA": [mtta_prom],
            "MTTR": [mttr_prom]
        }
        
        return pd.DataFrame(resumen)
    
    except Exception as e:
        print(f"Error al obtener el resumen de la línea {linea}: {e}")
        return pd.DataFrame()
# Función para obtener un resumen total de todas las líneas
def obtener_datos_resumen_total(start_date=None, end_date=None):
    resumen = []
    for linea, sistemas in datos_json.items():
        disponibilidad = confiabilidad = mtbf = mtta = mttr = 0
        
        for sistema, valores in sistemas.items():
            sistema_data = valores[0]
            fecha = pd.to_datetime(sistema_data.get('Fecha', None))
            if start_date and end_date:
                if fecha and (fecha < start_date or fecha > end_date):
                    continue  # Saltar datos fuera del rango
            disponibilidad += sistema_data.get("Disponibilidad", 0)
            confiabilidad += sistema_data.get("Confiabilidad", 0)
            mtbf += float(sistema_data.get("MTBF", 0))

        num_sistemas = len(sistemas)
        resumen.append({
            "Línea": linea,
            "Disponibilidad": disponibilidad / num_sistemas if num_sistemas > 0 else 0,
            "Confiabilidad": confiabilidad / num_sistemas if num_sistemas > 0 else 0,
            "MTBF": mtbf / num_sistemas if num_sistemas > 0 else 0,
            "MTTA": "00:00:00",
            "MTTR": "00:00:00"
        })
    
    return pd.DataFrame(resumen)

# Layout de la aplicación
layout = html.Div([
    html.H1('Indicadores por líneas', style=STYLE_CENTER),

    html.Div([
        html.Label('Selecciona Línea:'),
        dcc.Dropdown(
            id='linea-dropdown-1',
                options=[
                {'label': 'Línea Roja', 'value': 'Roja'},
                {'label': 'Línea Verde', 'value': 'Verde'},
                {'label': 'Línea Amarilla', 'value': 'Amarilla'},
                {'label': 'Línea Azul', 'value': 'Azul'},
                {'label': 'Línea Naranja', 'value': 'Naranja'},
                {'label': 'Línea Blanca', 'value': 'Blanca'},
                {'label': 'Línea Celeste', 'value': 'Celeste'},
                {'label': 'Línea Morada', 'value': 'Morada'},
                {'label': 'Línea Plateada', 'value': 'Plateada'},
                {'label': 'Línea Café', 'value': 'Cafe'},
                {'label': 'Resumen Total', 'value': 'resumentotal'}
            ],
            value='Roja',
            clearable=False
        ),
    ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

    html.Div([
        html.Label('Selecciona Sección:'),
        dcc.Dropdown(
            id='seccion-dropdown-1',
            options=[{'label': key, 'value': key} for key in SECCIONES.keys()],
            value='DISPONIBILIDAD',
            clearable=False
        ),
    ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

    html.Div([
        html.Label('Selecciona Rango de Fechas:'),
        dcc.DatePickerRange(
            id='date-picker-range-1',
            start_date='2024-06-01',
            end_date='2024-07-01',
            display_format='DD/MM/YYYY'
        ),
        html.Button('Generar la fecha', id='generar-fecha-button-1', n_clicks=0)
    ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(id='histograma-linea-1', style={**STYLE_INLINE_BLOCK, 'width': '85%', 'textAlign': 'center'}),
        
        html.Div([
            html.Label('Selecciona Sistemas:'),
            dcc.Checklist(
                id='sistemas-checklist-1',
                value=[],
                inline=False
            ),
            html.Br(),
            html.Label('Selecciona el tipo de gráfico:'),
            dcc.Dropdown(
                id='tipo-grafico-1',
                options=[
                    {'label': 'Barras Apiladas', 'value': 'bar_stacked'},
                    {'label': 'Columnas Apiladas', 'value': 'col_stacked'},
                    {'label': 'Barras Agrupadas', 'value': 'bar_grouped'},
                    {'label': 'Columnas Agrupadas', 'value': 'col_grouped'},
                    {'label': 'Gráfico de Líneas', 'value': 'line'}
                ],
                value='bar_stacked',
                clearable=False
            ),
            html.Br(),
            html.Button('Exportar a PDF', id='export-pdf-button-1', n_clicks=0)
        ], style={**STYLE_INLINE_BLOCK, 'width': '15%', 'paddingLeft': '10px', 'textAlign': 'left'})
    ], style={'display': 'flex', 'justifyContent':'center', 'alignItems': 'center'}),

    html.Div([
        html.H2('Resumen de Indicadores por Línea', style=STYLE_CENTER),
        dash_table.DataTable(
            id='tabla-linea-1',
            columns=[],
            data=[],
            style_table=STYLE_TABLE,
            style_cell=STYLE_CELL,
            style_header=STYLE_HEADER,
        )
    ], style={'marginTop': '20px', 'textAlign': 'center'}),

    html.Div([
        html.H2('Resumen de Indicadores por Promedios', style=STYLE_CENTER),
        dash_table.DataTable(
            id='tabla-resumen-1',
            columns=[],
            data=[],
            style_table=STYLE_TABLE,
            style_cell=STYLE_CELL,
            style_header=STYLE_HEADER,
        )
    ], style={'marginTop': '20px', 'textAlign': 'center'}),
    dcc.Download(id='download-pdf-1')
], style=STYLE_CENTER)

# Modificación en el callback de actualización de sección
@callback(
    [Output('sistemas-checklist-1', 'options'),
     Output('sistemas-checklist-1', 'value'),
     Output('tabla-linea-1', 'columns'),
     Output('tabla-linea-1', 'data')],
    [Input('linea-dropdown-1', 'value'),
     Input('seccion-dropdown-1', 'value'),
     Input('date-picker-range-1', 'start_date'),
     Input('date-picker-range-1', 'end_date')]
)
def actualizar_seccion(linea, seccion, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if linea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total(start_date, end_date)
        sistemas = df_resumen_total['Línea'].tolist()
        columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
        data = df_resumen_total.to_dict('records')
        return [{'label': line, 'value': line} for line in sistemas], sistemas, columns, data
    else:
        df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion], start_date, end_date)  # Llamada con fechas
        if df_seccion.empty:
            return [], [], [], []
        sistemas = df_seccion['Sistema'].tolist()
        columns = [{'name': col, 'id': col} for col in df_seccion.columns]
        data = df_seccion.to_dict('records')
        return [{'label': sistema, 'value': sistema} for sistema in sistemas], sistemas, columns, data

# # Callback para actualizar el gráfico
# @callback(
#     Output('histograma-linea-1', 'figure'),
#     [Input('generar-fecha-button-1', 'n_clicks')],  # Solo se ejecuta al presionar el botón
#     [State('sistemas-checklist-1', 'value'),
#      State('tipo-grafico-1', 'value'),
#      State('linea-dropdown-1', 'value'),
#      State('seccion-dropdown-1', 'value'),
#      State('date-picker-range-1', 'start_date'),
#      State('date-picker-range-1', 'end_date')]
# )
# # Callback para actualizar el gráfico
# Modificación en el callback para actualizar el gráfico
@callback(
    Output('histograma-linea-1', 'figure'),
    [Input('generar-fecha-button-1', 'n_clicks')],
    [State('sistemas-checklist-1', 'value'),
     State('tipo-grafico-1', 'value'),
     State('linea-dropdown-1', 'value'),
     State('seccion-dropdown-1', 'value'),
     State('date-picker-range-1', 'start_date'),
     State('date-picker-range-1', 'end_date')]
)
def update_histogram(n_clicks, selected_sistemas, tipo_grafico, linea, seccion, start_date, end_date):
    if n_clicks is None or n_clicks == 0:
        return go.Figure()  # No se ha presionado el botón, no se genera el gráfico

    # Convertir las fechas a formato datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    fig = go.Figure()

    if linea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total(start_date, end_date)  # Llamada con fechas
        filtered_df = df_resumen_total[df_resumen_total['Línea'].isin(selected_sistemas)]

        if filtered_df.empty:
            return fig  # Retornar gráfico vacío si no hay datos

        # Crear el gráfico basado en el tipo seleccionado
        for col in df_resumen_total.columns[1:]:
            if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                fig.add_trace(go.Bar(x=filtered_df['Línea'], y=filtered_df[col], name=col))
            elif tipo_grafico in ['col_stacked', 'col_grouped']:
                fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df['Línea'], name=col, orientation='h'))
            elif tipo_grafico == 'line':
                fig.add_trace(go.Scatter(x=filtered_df['Línea'], y=filtered_df[col], mode='lines+markers', name=col))
    else:
        df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion], start_date, end_date)  # Llamada con fechas
        filtered_df = df_seccion[df_seccion['Sistema'].isin(selected_sistemas)]

        if filtered_df.empty:
            return fig  # Retornar gráfico vacío si no hay datos

        # Crear el gráfico para los sistemas seleccionados
        for sistema in filtered_df['Sistema'].unique():
            sistema_df = filtered_df[filtered_df['Sistema'] == sistema]
            if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                fig.add_trace(go.Bar(x=[sistema], y=sistema_df['Valor'], name=sistema))
            elif tipo_grafico == 'line':
                fig.add_trace(go.Scatter(x=sistema_df['Fecha'], y=sistema_df['Valor'], mode='lines+markers', name=sistema))

    # Configuración de layout del gráfico
    fig.update_layout(barmode='stack', yaxis_title='Valores', xaxis_title='Sistemas')
    return fig

# Callback para exportar el gráfico a PDF
@callback(
    Output('download-pdf-1', 'data'),
    [Input('export-pdf-button-1', 'n_clicks')],
    [State('histograma-linea-1', 'figure')]
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

# Callback para actualizar la tabla de resumen de datos
@callback(
    [Output('tabla-resumen-1', 'columns'),
     Output('tabla-resumen-1', 'data')],
    [Input('linea-dropdown-1', 'value'),
     Input('date-picker-range-1', 'start_date'),
     Input('date-picker-range-1', 'end_date')]
)
def update_resumen_promedios(linea, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_resumen_promedios = obtener_datos_resumen_promedio_linea(linea)
    if not df_resumen_promedios.empty:
        columns = [{'name': col, 'id': col} for col in df_resumen_promedios.columns]
        data = df_resumen_promedios.to_dict('records')
        return columns, data
    return [], []
