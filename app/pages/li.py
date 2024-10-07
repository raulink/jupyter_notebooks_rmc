# import io
# import plotly.io as pio
# import dash
# from dash import dcc, html, Input, Output, State, callback
# from dash import dash_table
# import plotly.graph_objects as go
# import pandas as pd

# # Constantes para configuraciones de estilos
# STYLE_CENTER = {'textAlign': 'center'}
# STYLE_INLINE_BLOCK = {'display': 'inline-block', 'verticalAlign': 'top'}
# STYLE_TABLE = {'overflowX': 'scroll'}
# STYLE_CELL = {'textAlign': 'center'}
# STYLE_HEADER = {'fontWeight': 'bold'}

# # Ruta al archivo JSON
# JSON_FILE = 'data.json'

# # Diccionario de secciones
# SECCIONES = {
#     'DISPONIBILIDAD': (0, 8),
#     'CONFIABILIDAD': (9, 17),
#     'TIEMPO MEDIO ENTRE FALLAS (MTBF)': (18, 26),
#     'TIEMPO MEDIO DE RESPUESTA (MTTA)': (27, 35),
#     'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)': (36, 44)
# }

# def obtener_datos_seccion(línea, seccion):
#     try:
#         df = pd.read_excel(EXCEL_FILE, sheet_name=línea, skiprows=0, usecols='A:H', nrows=44)
#     except FileNotFoundError:
#         raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
#     except Exception as e:
#         raise Exception(f"Error al leer el archivo de Excel: {e}")
    
#     start_row, end_row = SECCIONES[seccion]
#     df_seccion = df.iloc[start_row:end_row].copy()

#     # Calcular el promedio o máximo según la sección
#     if seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
#         df_seccion.iloc[:, 1:] = df_seccion.iloc[:, 1:].stack().apply(
#             lambda x: x.hour * 3600 + x.minute * 60 + x.second).unstack()
        
#         if seccion == 'TIEMPO MEDIO DE RESPUESTA (MTTA)':
#             df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].mean(axis=1)
#         else:
#             df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].max(axis=1)
        
#         df_seccion['PROMEDIO'] = pd.to_datetime(df_seccion['PROMEDIO'], unit='s').dt.time
#     else:
#         df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].mean(axis=1)

#     return df_seccion

# def obtener_datos_resumen_total():
#     try:
#         df_resumen_total = pd.read_excel(EXCEL_FILE, sheet_name='resumentotal', skiprows=8, usecols='B:F', nrows=11)
#     except FileNotFoundError:
#         raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
#     except Exception as e:
#         raise Exception(f"Error al leer el archivo de Excel: {e}")
    
#     df_resumen_total.columns = ['DISPONIBILIDAD', 'CONFIABILIDAD', 'MTBF', 'MTTA', 'MTTR']
#     df_resumen_total.insert(0, 'Línea', ['Línea Roja', 'Línea Verde', 'Línea Amarilla', 'Línea Azul', 'Línea Naranja', 
#                                          'Línea Blanca', 'Línea Celeste', 'Línea Morada', 'Línea Plateada', 'Línea Café'])

#     return df_resumen_total

# def obtener_datos_tabla(línea):
#     try:
#         df = pd.read_excel(EXCEL_FILE, sheet_name=línea, usecols='J:N', nrows=2, header=None)
#     except FileNotFoundError:
#         raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
#     except Exception as e:
#         raise Exception(f"Error al leer el archivo de Excel: {e}")
    
#     # Los encabezados están en la primera fila (fila 0) y los datos en la segunda fila (fila 1)
#     headers = df.iloc[0].tolist()
#     values = df.iloc[1].tolist()
    
#     return headers, values

# # Layout de la aplicación
# layout = html.Div([
#     html.H1('2 indicadores por lineas', style=STYLE_CENTER),

#     html.Div([
#         html.Label('Selecciona Línea:'),
#         dcc.Dropdown(
#             id='linea-dropdown-1',
#             options=[
#                 {'label': 'Línea Roja', 'value': 'linearoja'},
#                 {'label': 'Línea Verde', 'value': 'lineaverde'},
#                 {'label': 'Línea Amarilla', 'value': 'lineaamarilla'},
#                 {'label': 'Línea Azul', 'value': 'lineaazul'},
#                 {'label': 'Línea Naranja', 'value': 'lineanaranja'},
#                 {'label': 'Línea Blanca', 'value': 'lineablanca'},
#                 {'label': 'Línea Celeste', 'value': 'lineaceleste'},
#                 {'label': 'Línea Morada', 'value': 'lineamorada'},
#                 {'label': 'Línea Plateada', 'value': 'lineaplateada'},
#                 {'label': 'Línea Café', 'value': 'lineacafe'},
#                 {'label': 'Resumen Total', 'value': 'resumentotal'}  # Nueva opción
#             ],
#             value='linearoja',
#             clearable=False
#         ),
#     ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

#     html.Div([
#         html.Label('Selecciona Sección:'),
#         dcc.Dropdown(
#             id='seccion-dropdown-1',
#             options=[{'label': key, 'value': key} for key in SECCIONES.keys()],
#             value='DISPONIBILIDAD',
#             clearable=False
#         ),
#     ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

#     html.Div([
#         dcc.Graph(id='histograma-linea-1', style={**STYLE_INLINE_BLOCK, 'width': '85%', 'textAlign': 'center'}),
        
#         html.Div([
#             html.Label('Selecciona Sistemas:'),
#             dcc.Checklist(
#                 id='sistemas-checklist-1',
#                 value=[],
#                 inline=False
#             ),
#             html.Br(),
#             html.Label('Selecciona el tipo de gráfico:'),
#             dcc.Dropdown(
#                 id='tipo-grafico-1',
#                 options=[
#                     {'label': 'Barras Apiladas', 'value': 'bar_stacked'},
#                     {'label': 'Columnas Apiladas', 'value': 'col_stacked'},
#                     {'label': 'Barras Agrupadas', 'value': 'bar_grouped'},
#                     {'label': 'Columnas Agrupadas', 'value': 'col_grouped'},
#                     {'label': 'Gráfico de Líneas', 'value': 'line'}
#                 ],
#                 value='bar_stacked',
#                 clearable=False
#             ),
#             html.Br(),
#             html.Button('Exportar a PDF', id='export-pdf-button-1', n_clicks=0)
#         ], style={**STYLE_INLINE_BLOCK, 'width': '15%', 'paddingLeft': '10px', 'textAlign': 'left'})
#     ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

#     html.Div([
#         html.H2('Resumen de Indicadores por Linea', style=STYLE_CENTER),
#         dash_table.DataTable(
#             id='tabla-linea-1',
#             columns=[],
#             data=[],
#             style_table=STYLE_TABLE,
#             style_cell=STYLE_CELL,
#             style_header=STYLE_HEADER,
#         )
#     ], style={'marginTop': '20px', 'textAlign': 'center'}),
#     html.Div([
#         html.H2('Resumen de Indicadores por Promedios', style=STYLE_CENTER),
#         dash_table.DataTable(
#             id='tabla-resumen-1',
#             columns=[],
#             data=[],
#             style_table=STYLE_TABLE,
#             style_cell=STYLE_CELL,
#             style_header=STYLE_HEADER,
#         )
#     ], style={'marginTop': '20px', 'textAlign': 'center'}),
#     dcc.Download(id='download-pdf-1')
# ], style=STYLE_CENTER)


# @callback(
#     [Output('sistemas-checklist-1', 'options'),
#      Output('sistemas-checklist-1', 'value'),
#      Output('tabla-linea-1', 'columns'),
#      Output('tabla-linea-1', 'data')],
#     [Input('linea-dropdown-1', 'value'),
#      Input('seccion-dropdown-1', 'value')]
# )
# def actualizar_seccion(línea, seccion):
#     if línea == 'resumentotal':
#         df_resumen_total = obtener_datos_resumen_total()
#         Sistemas = df_resumen_total['Línea'].tolist()
#         columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
#         data = df_resumen_total.to_dict('records')
#         return [{'label': line, 'value': line} for line in Sistemas], Sistemas, columns, data
#     else:
#         df_seccion = obtener_datos_seccion(línea, seccion)
#         Sistemas = df_seccion.iloc[:, 0].tolist()
#         columns = [{'name': col, 'id': col} for col in df_seccion.columns]
#         data = df_seccion.to_dict('records')
#         return [{'label': line, 'value': line} for line in Sistemas], Sistemas, columns, data

# @callback(
#     Output('histograma-linea-1', 'figure'),
#     [Input('sistemas-checklist-1', 'value'),
#      Input('tipo-grafico-1', 'value'),
#      Input('linea-dropdown-1', 'value'),
#      Input('seccion-dropdown-1', 'value')]
# )
# def update_histogram(selected_Sistemas, tipo_grafico, línea, seccion):
#     fig = go.Figure()

#     # Determinar el modo de apilado o agrupado para gráficos de barras o columnas
#     if tipo_grafico in ['bar_stacked', 'col_stacked']:
#         barmode = 'stack'
#     elif tipo_grafico in ['bar_grouped', 'col_grouped']:
#         barmode = 'group'
#     else:
#         barmode = None  # No apilamiento para gráficos de líneas
    
#     if línea == 'resumentotal':
#         df_resumen_total = obtener_datos_resumen_total()
#         filtered_df = df_resumen_total[df_resumen_total['Línea'].isin(selected_Sistemas)]
        
#         if seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
#             for col in ['MTTA', 'MTTR']:
#                 if col in filtered_df.columns:
#                     if tipo_grafico == 'line':
#                         fig.add_trace(go.Scatter(
#                             x=filtered_df['Línea'],
#                             y=filtered_df[col],
#                             mode='lines+markers',
#                             name=col
#                         ))
#                     else:
#                         fig.add_trace(go.Bar(
#                             x=filtered_df['Línea'] if tipo_grafico.startswith('bar') else filtered_df[col],
#                             y=filtered_df[col] if tipo_grafico.startswith('bar') else filtered_df['Línea'],
#                             name=col,
#                             orientation='h' if tipo_grafico.startswith('col') else 'v'
#                         ))

#             # Ajustar el eje Y para MTTA y MTTR en segundos
#             min_val = filtered_df[['MTTA', 'MTTR']].min().min()
#             max_val = filtered_df[['MTTA', 'MTTR']].max().max()

#             tickvals = list(range(int(min_val), int(max_val) + 1, max(1, int((max_val - min_val) / 8))))
#             ticktext = [pd.to_datetime(val, unit='s').strftime('%H:%M:%S') for val in tickvals]

#             fig.update_yaxes(
#                 range=[min_val, max_val],
#                 tickvals=tickvals,
#                 ticktext=ticktext,
#                 autorange="reversed"  # Esto asegura que el eje Y esté en orden ascendente
#             )
#         else:
#             for col in df_resumen_total.columns[1:]:
#                 if tipo_grafico in ['bar_stacked', 'bar_grouped']:
#                     fig.add_trace(go.Bar(x=filtered_df['Línea'], y=filtered_df[col], name=col))
#                 elif tipo_grafico in ['col_stacked', 'col_grouped']:
#                     fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df['Línea'], name=col, orientation='h'))
#                 elif tipo_grafico == 'line':
#                     fig.add_trace(go.Scatter(x=filtered_df['Línea'], y=filtered_df[col], mode='lines+markers', name=col))

#     else:
#         df_seccion = obtener_datos_seccion(línea, seccion)
#         filtered_df = df_seccion[df_seccion.iloc[:, 0].isin(selected_Sistemas)]

#         for col in df_seccion.columns[1:-1]:
#             if tipo_grafico in ['bar_stacked', 'bar_grouped']:
#                 fig.add_trace(go.Bar(x=filtered_df.iloc[:, 0], y=filtered_df[col], name=col))
#             elif tipo_grafico in ['col_stacked', 'col_grouped']:
#                 fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df.iloc[:, 0], name=col, orientation='h'))
#             elif tipo_grafico == 'line':
#                 fig.add_trace(go.Scatter(x=filtered_df.iloc[:, 0], y=filtered_df[col], mode='lines+markers', name=col))
        
#         # Trazado para la columna de "PROMEDIO"
#         fig.add_trace(go.Scatter(
#             x=filtered_df.iloc[:, 0],
#             y=filtered_df['PROMEDIO'],
#             mode='lines+markers' if tipo_grafico == 'line' else 'markers',
#             name='PROMEDIO',
#             line=dict(color='orange', width=4, dash='dash') if tipo_grafico == 'line' else None,
#             marker_color='orange' if tipo_grafico != 'line' else None
#         ))

#         # Configuración del eje Y basada en la sección seleccionada
#         if seccion == 'DISPONIBILIDAD':
#             fig.update_yaxes(
#             range=[0.9, 1.0],
#             tickformat=".0%",
#             tickvals=[0.90 + i * 0.02 for i in range(6)],  # Incrementos de 2.0%
#             ticktext=[f"{0.90 + i * 0.02:.1%}" for i in range(6)]
#             )
#         elif seccion == 'CONFIABILIDAD':
            
#             min_val = filtered_df.iloc[:, 1:-1].min().min()
#             max_val = 1.0  # 100.0% en formato decimal

#             if min_val < 0:
#                 min_val = min_val
        
#             fig.update_yaxes(
#                 range=[min_val, max_val],
#                 tickformat=".0%",
#                 tickvals=[i * 0.2 for i in range(int(max_val * 5 + 1))],  # Incrementos de 20.0%
#                 ticktext=[f"{i * 20:.0f}%" for i in range(int(max_val * 5 + 1))]
#             )
#         elif seccion in ['TIEMPO MEDIO ENTRE FALLAS (MTBF)']:
#             y_max = filtered_df.iloc[:, 1:-1].values.max()
#             y_min = filtered_df.iloc[:, 1:-1].values.min()
#             fig.update_yaxes(range=[y_min, y_max])
        
#         elif seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
#             y_max = filtered_df.iloc[:, 1:-1].max().max()
#             y_min = filtered_df.iloc[:, 1:-1].min().min()
        
#             # Generar los valores de tickvals y ticktext como listas
#             tickvals = list(range(int(y_min), int(y_max) + 1, max(1, int((y_max - y_min) / 8))))
#             ticktext = [pd.to_datetime(val, unit='s').strftime('%H:%M:%S') for val in tickvals]
        
#             fig.update_yaxes(
#                 range=[y_min, y_max],
#                 tickvals=tickvals,
#                 ticktext=ticktext
#             )

#     fig.update_layout(barmode=barmode, yaxis_title='Valores', xaxis_title='Sistemas')
#     return fig


# @callback(
#     Output('download-pdf-1', 'data'),
#     [Input('export-pdf-button-1', 'n_clicks')],
#     [State('histograma-linea-1', 'figure')]
# )
# def export_to_pdf(n_clicks, fig):
#     if n_clicks > 0:
#         if fig:
#             # Convertir el gráfico a PDF
#             buffer = io.BytesIO()
#             pio.write_image(fig, buffer, format='pdf')
#             buffer.seek(0)
#             return dcc.send_bytes(buffer.getvalue(), 'grafico.pdf')
#     return None


# @callback(
#     [Output('tabla-resumen-1', 'columns'),
#      Output('tabla-resumen-1', 'data')],
#     [Input('linea-dropdown-1', 'value')]
# )
# def update_table(línea):
#     if línea == 'resumentotal':
#         df_resumen_total = obtener_datos_resumen_total()
#         columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
#         data = df_resumen_total.to_dict('records')
#     else:
#         headers, values = obtener_datos_tabla(línea)
#         columns = [{'name': header, 'id': header} for header in headers]
#         data = [dict(zip(headers, values))]
    
#     return columns, data
#---------------------------------------------------------------------------------------------------------------------------

import json
import io
import plotly.io as pio
import dash
from dash import dcc, html, Input, Output, State, callback
from dash import dash_table
import plotly.graph_objects as go
import pandas as pd

# Constantes para configuraciones de estilos
STYLE_CENTER = {'textAlign': 'center'}
STYLE_INLINE_BLOCK = {'display': 'inline-block', 'verticalAlign': 'top'}
STYLE_TABLE = {'overflowX': 'scroll'}
STYLE_CELL = {'textAlign': 'center'}
STYLE_HEADER = {'fontWeight': 'bold'}

# Ruta al archivo JSON
JSON_FILE = 'data.json'

def cargar_datos_json(json_file):
    with open(json_file, 'r') as file:
        datos = json.load(file)
    return datos

# Cargar los datos del archivo JSON
datos_json = cargar_datos_json(JSON_FILE)

# Diccionario de secciones
SECCIONES = {
    'DISPONIBILIDAD': 'Disponibilidad',
    'CONFIABILIDAD': 'Confiabilidad',
    'TIEMPO MEDIO ENTRE FALLAS (MTBF)': 'MTBF',
    'TIEMPO MEDIO DE RESPUESTA (MTTA)': 'MTTA',
    'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)': 'MTTR'
}

# Función para obtener los datos de una sección específica de una línea
def obtener_datos_seccion(linea, seccion):
    try:
        secciones = datos_json.get(linea, {})
        if not secciones:
            print(f"No se encontró la línea {linea} en los datos.")
            return pd.DataFrame()
        
        datos_seccion = []
        for sistema, valores in secciones.items():
            for valor in valores:
                datos_seccion.append({
                    'Sistema': sistema,
                    'Valor': valor[seccion]
                })
        
        df_seccion = pd.DataFrame(datos_seccion)
        return df_seccion
    except Exception as e:
        print(f"Error al obtener datos de la sección {seccion} en la línea {linea}: {e}")
        return pd.DataFrame()

# Función para obtener un resumen total de todas las líneas
def obtener_datos_resumen_total():
    resumen = []
    for linea, sistemas in datos_json.items():
        disponibilidad = confiabilidad = mtbf = mtta = mttr = 0
        
        for sistema, valores in sistemas.items():
            sistema_data = valores[0]
            disponibilidad += sistema_data.get("Disponibilidad", 0)
            confiabilidad += sistema_data.get("Confiabilidad", 0)
            mtbf += float(sistema_data.get("MTBF", 0))

        num_sistemas = len(sistemas)
        resumen.append({
            "Línea": linea,
            "Disponibilidad": disponibilidad / num_sistemas,
            "Confiabilidad": confiabilidad / num_sistemas,
            "MTBF": mtbf / num_sistemas,
            "MTTA": "00:00:00",
            "MTTR": "00:00:00"
        })
    
    return pd.DataFrame(resumen)

# Layout de la aplicación
layout = html.Div([
    html.H1('2 indicadores por lineas', style=STYLE_CENTER),

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
        html.Label('Selecciona Fecha:'),
        dcc.Dropdown(
            id='fecha-dropdown-1',
            options=[
                {'label': 'Enero', 'value': 'Enero'},
                {'label': 'Febrero', 'value': 'Febrero'},
                {'label': 'Marzo', 'value': 'Marzo'},
                {'label': 'Abril', 'value': 'Abril'},
                {'label': 'Mayo', 'value': 'Mayo'},
                {'label': 'Junio', 'value': 'Junio'},
                {'label': 'Promedio', 'value': 'Promedio'}
            ],
            value='Promedio',
            clearable=False
        ),
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
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

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

# Callback para actualizar las secciones de sistemas y las tablas
@callback(
    [Output('sistemas-checklist-1', 'options'),
     Output('sistemas-checklist-1', 'value'),
     Output('tabla-linea-1', 'columns'),
     Output('tabla-linea-1', 'data')],
    [Input('linea-dropdown-1', 'value'),
     Input('seccion-dropdown-1', 'value')]
)
def actualizar_seccion(linea, seccion):
    if linea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        sistemas = df_resumen_total['Línea'].tolist()
        columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
        data = df_resumen_total.to_dict('records')
        return [{'label': line, 'value': line} for line in sistemas], sistemas, columns, data
    else:
        df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion])
        if df_seccion.empty:
            return [], [], [], []
        sistemas = df_seccion['Sistema'].tolist()
        columns = [{'name': col, 'id': col} for col in df_seccion.columns]
        data = df_seccion.to_dict('records')
        return [{'label': sistema, 'value': sistema} for sistema in sistemas], sistemas, columns, data

# Callback para actualizar el gráfico
@callback(
    Output('histograma-linea-1', 'figure'),
    [Input('sistemas-checklist-1', 'value'),
     Input('tipo-grafico-1', 'value'),
     Input('linea-dropdown-1', 'value'),
     Input('seccion-dropdown-1', 'value'),
     Input('fecha-dropdown-1', 'value')] # Añadimos la nueva entrada de la fecha
)
def update_histogram(selected_sistemas, tipo_grafico, linea, seccion, fecha):
    fig = go.Figure()

        # Configurar el modo de apilamiento o agrupado
    if tipo_grafico in ['bar_stacked', 'col_stacked']:
        barmode = 'stack'
    elif tipo_grafico in ['bar_grouped', 'col_grouped']:
        barmode = 'group'
    else:
        barmode = None
    # Obtener los datos según la línea y la sección seleccionada
    if linea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        filtered_df = df_resumen_total[df_resumen_total['Línea'].isin(selected_sistemas)]

        # Crear el gráfico
        for col in df_resumen_total.columns[1:]:
            if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                fig.add_trace(go.Bar(x=filtered_df['Línea'], y=filtered_df[col], name=col))
            elif tipo_grafico in ['col_stacked', 'col_grouped']:
                fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df['Línea'], name=col, orientation='h'))
            elif tipo_grafico == 'line':
                fig.add_trace(go.Scatter(x=filtered_df['Línea'], y=filtered_df[col], mode='lines+markers', name=col))
    else:
        df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion])
        if df_seccion.empty:
            return fig

        filtered_df = df_seccion[df_seccion['Sistema'].isin(selected_sistemas)]

        for sistema in filtered_df['Sistema'].unique():
            sistema_df = filtered_df[filtered_df['Sistema'] == sistema]
            if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                fig.add_trace(go.Bar(x=[sistema], y=sistema_df['Valor'], name=sistema))
            elif tipo_grafico == 'line':
                fig.add_trace(go.Scatter(x=[sistema], y=sistema_df['Valor'], mode='lines+markers', name=sistema))

    fig.update_layout(barmode=barmode, yaxis_title='Valores', xaxis_title='Sistemas')
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
    [Input('linea-dropdown-1', 'value')]
)
def update_table(linea):
    if linea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
        data = df_resumen_total.to_dict('records')
    else:
        df_seccion = obtener_datos_seccion(linea, 'Disponibilidad')  # Cambiar sección según lo que necesites
        if df_seccion.empty:
            return [], []
        columns =[{'name': 'Sistema', 'id': 'Sistema'}, {'name': 'Disponibilidad', 'id': 'Valor'}]
        data = df_seccion[['Sistema', 'Valor']].to_dict('records')
    
    return columns, data


# import json
# import requests  # Asegúrate de tener instalado requests
# import io
# import plotly.io as pio
# import dash
# from dash import dcc, html, Input, Output, State, callback
# from dash import dash_table
# import plotly.graph_objects as go
# import pandas as pd
# from datetime import datetime

# # Constantes para configuraciones de estilos
# STYLE_CENTER = {'textAlign': 'center'}
# STYLE_INLINE_BLOCK = {'display': 'inline-block', 'verticalAlign': 'top'}
# STYLE_TABLE = {'overflowX': 'scroll'}
# STYLE_CELL = {'textAlign': 'center'}
# STYLE_HEADER = {'fontWeight': 'bold'}

# # URL que contiene los datos en formato JSON
# URL_JSON = 'https://operaciones.miteleferico.bo/API/total/sistemas/2024-06-01/2024-07-01'

# def cargar_datos_json(url):
#     try:
#         # Realizamos la solicitud GET a la URL
#         response = requests.get(url)
#         # Comprobamos que la solicitud haya sido exitosa
#         response.raise_for_status()
#         # Convertimos la respuesta a formato JSON
#         datos = response.json()
#         return datos
#     except requests.exceptions.RequestException as e:
#         print(f"Error al obtener los datos de la URL: {e}")
#         return {}

# # Cargar los datos desde la URL
# datos_json = cargar_datos_json(URL_JSON)

# # Diccionario de secciones
# SECCIONES = {
#     'DISPONIBILIDAD': 'Disponibilidad',
#     'CONFIABILIDAD': 'Confiabilidad',
#     'TIEMPO MEDIO ENTRE FALLAS (MTBF)': 'MTBF',
#     'TIEMPO MEDIO DE RESPUESTA (MTTA)': 'MTTA',
#     'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)': 'MTTR'
# }

# # Función para obtener los datos de una sección específica de una línea con filtro de fecha
# def obtener_datos_seccion(linea, seccion, fecha_inicio=None, fecha_fin=None):
#     try:
#         secciones = datos_json.get(linea, {})
#         if not secciones:
#             print(f"No se encontró la línea {linea} en los datos.")
#             return pd.DataFrame()

#         datos_seccion = []
#         for sistema, valores in secciones.items():
#             for valor in valores:
#                 # Asegurarse de que 'Fecha' existe en los datos
#                 fecha_str = valor.get('Fecha', None)
#                 if fecha_str:
#                     fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
#                     # Filtrar por rango de fechas si se proporcionan
#                     if fecha_inicio and fecha_fin:
#                         if fecha_inicio <= fecha <= fecha_fin:
#                             datos_seccion.append({
#                                 'Sistema': sistema,
#                                 'Valor': valor[seccion],
#                                 'Fecha': fecha
#                             })
#                     else:
#                         datos_seccion.append({
#                             'Sistema': sistema,
#                             'Valor': valor[seccion],
#                             'Fecha': fecha
#                         })
#                 else:
#                     # Si no hay fecha, incluir el dato sin filtrar por fecha
#                     datos_seccion.append({
#                         'Sistema': sistema,
#                         'Valor': valor[seccion],
#                         'Fecha': None
#                     })

#         df_seccion = pd.DataFrame(datos_seccion)
#         return df_seccion
#     except Exception as e:
#         print(f"Error al obtener datos de la sección {seccion} en la línea {linea}: {e}")
#         return pd.DataFrame()

# # Función para obtener un resumen total de todas las líneas
# def obtener_datos_resumen_total(fecha_inicio=None, fecha_fin=None):
#     resumen = []
#     for linea, sistemas in datos_json.items():
#         disponibilidad = confiabilidad = mtbf = 0
#         num_sistemas = 0

#         for sistema, valores in sistemas.items():
#             for valor in valores:
#                 # Asegurarse de que 'Fecha' existe en los datos
#                 fecha_str = valor.get('Fecha', None)
#                 if fecha_str:
#                     fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
#                     # Filtrar por rango de fechas si se proporcionan
#                     if fecha_inicio and fecha_fin:
#                         if not (fecha_inicio <= fecha <= fecha_fin):
#                             continue  # Saltar si no está en el rango de fechas
#                 else:
#                     # Si no hay fecha, no se puede filtrar, así que saltamos
#                     continue

#                 disponibilidad += valor.get("Disponibilidad", 0)
#                 confiabilidad += valor.get("Confiabilidad", 0)
#                 mtbf += float(valor.get("MTBF", 0))
#                 num_sistemas += 1
#                 break  # Solo tomar el primer valor por sistema para evitar duplicados

#         if num_sistemas > 0:
#             resumen.append({
#                 "Línea": linea,
#                 "Disponibilidad": disponibilidad / num_sistemas,
#                 "Confiabilidad": confiabilidad / num_sistemas,
#                 "MTBF": mtbf / num_sistemas,
#                 "MTTA": "00:00:00",  # Puedes ajustar esto si es necesario
#                 "MTTR": "00:00:00"   # Puedes ajustar esto si es necesario
#             })

#     return pd.DataFrame(resumen)

# def obtener_datos_resumen_promedio_linea(linea, fecha_inicio=None, fecha_fin=None):
#     try:
#         # Obtiene los sistemas de la línea seleccionada
#         sistemas = datos_json.get(linea, {})
#         disponibilidad_total = 0
#         confiabilidad_total = 0
#         mtbf_total = 0
#         mtta_total = pd.to_timedelta('00:00:00')
#         mttr_total = pd.to_timedelta('00:00:00')
#         num_sistemas = 0

#         for sistema, valores in sistemas.items():
#             for valor in valores:
#                 # Asegurarse de que 'Fecha' existe en los datos
#                 fecha_str = valor.get('Fecha', None)
#                 if fecha_str:
#                     fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
#                     # Filtrar por rango de fechas si se proporcionan
#                     if fecha_inicio and fecha_fin:
#                         if not (fecha_inicio <= fecha <= fecha_fin):
#                             continue  # Saltar si no está en el rango de fechas
#                 else:
#                     # Si no hay fecha, no se puede filtrar, así que saltamos
#                     continue

#                 # Sumar los valores para cada métrica
#                 disponibilidad_total += valor.get("Disponibilidad", 0)
#                 confiabilidad_total += valor.get("Confiabilidad", 0)
#                 mtbf_total += float(valor.get("MTBF", 0))
#                 mtta_total += pd.to_timedelta(valor.get("MTTA", "00:00:00"))
#                 mttr_total += pd.to_timedelta(valor.get("MTTR", "00:00:00"))
#                 num_sistemas += 1
#                 break  # Solo tomar el primer valor por sistema para evitar duplicados

#         if num_sistemas > 0:
#             # Calcular los promedios finales
#             disponibilidad_prom = disponibilidad_total / num_sistemas
#             confiabilidad_prom = confiabilidad_total / num_sistemas
#             mtbf_prom = mtbf_total / num_sistemas
#             mtta_prom = str(mtta_total / num_sistemas)
#             mttr_prom = str(mttr_total / num_sistemas)

#             # Devolver los promedios en formato DataFrame
#             resumen = {
#                 "Disponibilidad": [disponibilidad_prom],
#                 "Confiabilidad": [confiabilidad_prom],
#                 "MTBF": [mtbf_prom],
#                 "MTTA": [mtta_prom],
#                 "MTTR": [mttr_prom]
#             }
#         else:
#             resumen = {
#                 "Disponibilidad": [],
#                 "Confiabilidad": [],
#                 "MTBF": [],
#                 "MTTA": [],
#                 "MTTR": []
#             }

#         return pd.DataFrame(resumen)

#     except Exception as e:
#         print(f"Error al obtener el resumen de la línea {linea}: {e}")
#         return pd.DataFrame()

# # Layout de la aplicación
# layout = html.Div([
#     html.H1('2 indicadores por líneas', style=STYLE_CENTER),

#     html.Div([
#         html.Label('Selecciona Línea:'),
#         dcc.Dropdown(
#             id='linea-dropdown-1',
#             options=[
#                 {'label': 'Línea Roja', 'value': 'Roja'},
#                 {'label': 'Línea Verde', 'value': 'Verde'},
#                 {'label': 'Línea Amarilla', 'value': 'Amarilla'},
#                 {'label': 'Línea Azul', 'value': 'Azul'},
#                 {'label': 'Línea Naranja', 'value': 'Naranja'},
#                 {'label': 'Línea Blanca', 'value': 'Blanca'},
#                 {'label': 'Línea Celeste', 'value': 'Celeste'},
#                 {'label': 'Línea Morada', 'value': 'Morada'},
#                 {'label': 'Línea Plateada', 'value': 'Plateada'},
#                 {'label': 'Línea Café', 'value': 'Cafe'},
#                 {'label': 'Resumen Total', 'value': 'resumentotal'}  
#             ],
#             value='Roja',
#             clearable=False
#         ),
#     ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

#     html.Div([
#         html.Label('Selecciona Sección:'),
#         dcc.Dropdown(
#             id='seccion-dropdown-1',
#             options=[{'label': key, 'value': key} for key in SECCIONES.keys()],
#             value='DISPONIBILIDAD',
#             clearable=False
#         ),
#     ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

#     # Añadimos el selector de rango de fechas
#     html.Div([
#         html.Label('Selecciona Rango de Fechas:'),
#         dcc.DatePickerRange(
#             id='date-picker-range-1',
#             start_date='2024-06-01',
#             end_date='2024-07-01',
#             display_format='DD/MM/YYYY'
#         ),
#     ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

#     html.Div([
#         dcc.Graph(id='histograma-linea-1', style={**STYLE_INLINE_BLOCK, 'width': '85%', 'textAlign': 'center'}),
        
#         html.Div([
#             html.Label('Selecciona Sistemas:'),
#             dcc.Checklist(
#                 id='sistemas-checklist-1',
#                 value=[],
#                 inline=False
#             ),
#             html.Br(),
#             html.Label('Selecciona el tipo de gráfico:'),
#             dcc.Dropdown(
#                 id='tipo-grafico-1',
#                 options=[
#                     {'label': 'Barras Apiladas', 'value': 'bar_stacked'},
#                     {'label': 'Columnas Apiladas', 'value': 'col_stacked'},
#                     {'label': 'Barras Agrupadas', 'value': 'bar_grouped'},
#                     {'label': 'Columnas Agrupadas', 'value': 'col_grouped'},
#                     {'label': 'Gráfico de Líneas', 'value': 'line'}
#                 ],
#                 value='bar_stacked',
#                 clearable=False
#             ),
#             html.Br(),
#             html.Button('Exportar a PDF', id='export-pdf-button-1', n_clicks=0)
#         ], style={**STYLE_INLINE_BLOCK, 'width': '15%', 'paddingLeft': '10px', 'textAlign': 'left'})
#     ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

#     html.Div([
#         html.H2('Resumen de Indicadores por Línea', style=STYLE_CENTER),
#         dash_table.DataTable(
#             id='tabla-linea-1',
#             columns=[],
#             data=[],
#             style_table=STYLE_TABLE,
#             style_cell=STYLE_CELL,
#             style_header=STYLE_HEADER,
#         )
#     ], style={'marginTop': '20px', 'textAlign': 'center'}),

#     html.Div([
#         html.H2('Resumen de Indicadores por Promedios', style=STYLE_CENTER),
#         dash_table.DataTable(
#             id='tabla-resumen-1',
#             columns=[],
#             data=[],
#             style_table=STYLE_TABLE,
#             style_cell=STYLE_CELL,
#             style_header=STYLE_HEADER,
#         )
#     ], style={'marginTop': '20px', 'textAlign': 'center'}),
#     dcc.Download(id='download-pdf-1')
# ], style=STYLE_CENTER)

# # Callback para actualizar las secciones de sistemas y las tablas
# @callback(
#     [Output('sistemas-checklist-1', 'options'),
#      Output('sistemas-checklist-1', 'value'),
#      Output('tabla-linea-1', 'columns'),
#      Output('tabla-linea-1', 'data')],
#     [Input('linea-dropdown-1', 'value'),
#      Input('seccion-dropdown-1', 'value'),
#      Input('date-picker-range-1', 'start_date'),
#      Input('date-picker-range-1', 'end_date')]
# )
# def actualizar_seccion(linea, seccion, start_date, end_date):
#     # Convertir las fechas de entrada a objetos datetime
#     fecha_inicio = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
#     fecha_fin = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

#     if linea == 'resumentotal':
#         df_resumen_total = obtener_datos_resumen_total(fecha_inicio, fecha_fin)
#         sistemas = df_resumen_total['Línea'].tolist()
#         columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
#         data = df_resumen_total.to_dict('records')
#         return [{'label': line, 'value': line} for line in sistemas], sistemas, columns, data
#     else:
#         df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion], fecha_inicio, fecha_fin)
#         if df_seccion.empty:
#             return [], [], [], []
#         sistemas = df_seccion['Sistema'].unique().tolist()
#         columns = [{'name': col, 'id': col} for col in df_seccion.columns]
#         data = df_seccion.to_dict('records')
#         return [{'label': sistema, 'value': sistema} for sistema in sistemas], sistemas, columns, data

# # Callback para actualizar el gráfico
# @callback(
#     Output('histograma-linea-1', 'figure'),
#     [Input('sistemas-checklist-1', 'value'),
#      Input('tipo-grafico-1', 'value'),
#      Input('linea-dropdown-1', 'value'),
#      Input('seccion-dropdown-1', 'value'),
#      Input('date-picker-range-1', 'start_date'),
#      Input('date-picker-range-1', 'end_date')]
# )
# def update_histogram(selected_sistemas, tipo_grafico, linea, seccion, start_date, end_date):
#     fig = go.Figure()

#     # Configurar el modo de apilamiento o agrupado
#     if tipo_grafico in ['bar_stacked', 'col_stacked']:
#         barmode = 'stack'
#     elif tipo_grafico in ['bar_grouped', 'col_grouped']:
#         barmode = 'group'
#     else:
#         barmode = None

#     # Convertir las fechas de entrada a objetos datetime
#     fecha_inicio = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
#     fecha_fin = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

#     # Obtener los datos según la línea y la sección seleccionada
#     if linea == 'resumentotal':
#         df_resumen_total = obtener_datos_resumen_total(fecha_inicio, fecha_fin)
#         filtered_df = df_resumen_total[df_resumen_total['Línea'].isin(selected_sistemas)]

#         # Crear el gráfico
#         for col in df_resumen_total.columns[1:]:
#             if tipo_grafico in ['bar_stacked', 'bar_grouped']:
#                 fig.add_trace(go.Bar(x=filtered_df['Línea'], y=filtered_df[col], name=col))
#             elif tipo_grafico in ['col_stacked', 'col_grouped']:
#                 fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df['Línea'], name=col, orientation='h'))
#             elif tipo_grafico == 'line':
#                 fig.add_trace(go.Scatter(x=filtered_df['Línea'], y=filtered_df[col], mode='lines+markers', name=col))
#     else:
#         df_seccion = obtener_datos_seccion(linea, SECCIONES[seccion], fecha_inicio, fecha_fin)
#         if df_seccion.empty:
#             return fig

#         filtered_df = df_seccion[df_seccion['Sistema'].isin(selected_sistemas)]

#         # Crear el gráfico según el tipo seleccionado
#         for sistema in filtered_df['Sistema'].unique():
#             sistema_df = filtered_df[filtered_df['Sistema'] == sistema]
#             if tipo_grafico in ['bar_stacked', 'bar_grouped']:
#                 fig.add_trace(go.Bar(x=[sistema], y=sistema_df['Valor'], name=sistema))
#             elif tipo_grafico == 'line':
#                 fig.add_trace(go.Scatter(x=[sistema], y=sistema_df['Valor'], mode='lines+markers', name=sistema))

#     fig.update_layout(barmode=barmode, yaxis_title='Valores', xaxis_title='Sistemas')
#     return fig

# # Callback para exportar el gráfico a PDF
# @callback(
#     Output('download-pdf-1', 'data'),
#     [Input('export-pdf-button-1', 'n_clicks')],
#     [State('histograma-linea-1', 'figure')]
# )
# def export_to_pdf(n_clicks, fig):
#     if n_clicks > 0:
#         if fig:
#             # Convertir el gráfico a PDF
#             buffer = io.BytesIO()
#             pio.write_image(fig, buffer, format='pdf')
#             buffer.seek(0)
#             return dcc.send_bytes(buffer.getvalue(), 'grafico.pdf')
#     return None

# # Callback para actualizar la tabla de resumen de promedios
# @callback(
#     [Output('tabla-resumen-1', 'columns'),
#      Output('tabla-resumen-1', 'data')],
#     [Input('linea-dropdown-1', 'value'),
#      Input('date-picker-range-1', 'start_date'),
#      Input('date-picker-range-1', 'end_date')]
# )
# def update_resumen_promedios(linea, start_date, end_date):
#     # Convertir las fechas de entrada a objetos datetime
#     fecha_inicio = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
#     fecha_fin = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

#     # Llamar a la función para obtener el resumen de promedios
#     df_resumen_promedios = obtener_datos_resumen_promedio_linea(linea, fecha_inicio, fecha_fin)
    
#     # Definir las columnas para la tabla
#     columns = [{'name': col, 'id': col} for col in df_resumen_promedios.columns]
    
#     # Convertir el DataFrame a un diccionario de registros
#     data = df_resumen_promedios.to_dict('records')
    
#     return columns, data


