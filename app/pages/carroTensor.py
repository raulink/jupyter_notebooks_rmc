# # # import pandas as pd
# # # import plotly.express as px
# # # from dash import dcc, html, Input, Output, callback
# # # import dash

# # # # Enlace CSV de Google Sheets actualizado
# # # CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQeyBubLucOlpCdHKSjPNdQtdxI89y8nxyJH3o-rYnHmSwFrezuzFIfmmcwnUuvLb66PvZ2TJjCyzgg/pub?output=csv'

# # # # Función para obtener los datos desde el enlace CSV de Google Sheets
# # # def obtener_datos_desde_csv():
# # #     try:
# # #         df = pd.read_csv(CSV_URL, header=0)
# # #         return df
# # #     except Exception as e:
# # #         print(f"Error al obtener datos desde CSV: {e}")
# # #         return pd.DataFrame()

# # # # Definir las opciones de periodo, línea y categoría
# # # time_options = ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']
# # # line_options = ['LINEA ROJA', 'LINEA AMARILLA', 'LINEA VERDE', 'LINEA AZUL', 'LINEA PLATEADA']
# # # category_options = ['S1R1', 'S2R1', 'S2R2', 'S1R2']

# # # # Mapeo de columnas para cada combinación de línea y categoría por periodo
# # # column_map = {
# # #     'MENSUAL 05': {
# # #         'LINEA ROJA': {'S1R1': 'E', 'S2R1': 'F'},
# # #         'LINEA AMARILLA': {'S1R1': 'G', 'S1R2': 'H', 'S2R2': 'I'},
# # #         'LINEA VERDE': {'S1R1': 'J', 'S2R1': 'K'},
# # #         'LINEA AZUL': {'S1R1': 'L', 'S2R1': 'M'},
# # #         'LINEA PLATEADA': {'S1R1': 'N', 'S2R1': 'O'}
# # #     },
# # #     # Agregar más periodos y líneas según tu archivo
# # #     'MENSUAL 06': {
# # #         'LINEA ROJA': {'S1R1': 'AB', 'S2R1': 'AC'},
# # #         'LINEA AMARILLA': {'S1R1': 'AD', 'S1R2': 'AE', 'S2R2': 'AF'},
# # #         'LINEA VERDE': {'S1R1': 'AG', 'S2R1': 'AH'},
# # #         'LINEA AZUL': {'S1R1': 'AI', 'S2R1': 'AJ'},
# # #         'LINEA PLATEADA': {'S1R1': 'AK', 'S2R1': 'AL'}
# # #     }
# # # }

# # # # Layout de la aplicación
# # # layout = html.Div([
# # #     html.H1('Dashboard de Carro Tensor'),

# # #     html.Div([
# # #         html.Label('Seleccione el periodo:'),
# # #         dcc.Dropdown(
# # #             id='tiempo-dropdown-6',
# # #             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
# # #             value=''  # Valor predeterminado
# # #         ),
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
# # #     html.Div([
# # #         html.Label('Seleccione la línea:'),
# # #         dcc.Dropdown(
# # #             id='linea-dropdown-6',
# # #             options=[{'label': linea, 'value': linea} for linea in line_options],
# # #             value=''  # Valor predeterminado
# # #         ),
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# # #     html.Div([
# # #         html.Label('Seleccione la categoría:'),
# # #         dcc.Dropdown(
# # #             id='categoria-dropdown-6',
# # #             options=[{'label': categoria, 'value': categoria} for categoria in category_options],
# # #             value='S1R1'  # Valor predeterminado
# # #         ),
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
# # #     html.Div([
# # #         html.Label('Seleccione el tipo de gráfico:'),
# # #         dcc.Dropdown(
# # #             id='tipo-grafico-dropdown-6',
# # #             options=[
# # #                 {'label': 'Barras', 'value': 'bar'},
# # #                 {'label': 'Líneas', 'value': 'line'},
# # #                 {'label': 'Torta', 'value': 'pie'},
# # #                 {'label': 'Área', 'value': 'area'},
# # #                 {'label': 'Dispersión', 'value': 'scatter'},
# # #                 {'label': 'Histograma', 'value': 'histogram'},
# # #                 {'label': 'Cajas', 'value': 'box'},
# # #                 {'label': 'Violín', 'value': 'violin'},
# # #                 {'label': 'Heatmap', 'value': 'heatmap'}
# # #             ],
# # #             value='bar'  # Valor predeterminado
# # #         ),
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# # #     html.Br(),  # Añadir separación visual

# # #     html.Div([
# # #         dcc.Graph(id='dashboard-6')
# # #     ], style={
# # #         'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
# # #         'padding': '20px',  # Añadir padding para mejor visualización
# # #         'border-radius': '10px'  # Añadir bordes redondeados
# # #     })
# # # ])

# # # # Callback para actualizar el gráfico basado en la selección de periodo, línea, categoría y tipo de gráfico
# # # @callback(
# # #     Output('dashboard-6', 'figure'),
# # #     [Input('tiempo-dropdown-6', 'value'),
# # #      Input('linea-dropdown-6', 'value'),
# # #      Input('categoria-dropdown-6', 'value'),
# # #      Input('tipo-grafico-dropdown-6', 'value')]
# # # )
# # # def update_dashboard(selected_time, selected_line, selected_category, selected_chart):
# # #     # Obtener los datos desde el CSV
# # #     df = obtener_datos_desde_csv()

# # #     # Verificar si la selección existe en el mapa de columnas
# # #     if selected_time in column_map and selected_line in column_map[selected_time]:
# # #         column = column_map[selected_time][selected_line].get(selected_category, None)

# # #         if column:
# # #             #
# # #             # Filtrar los datos de las filas 7 a 16 (ajustar según necesidad)
# # #             df_filtered = df.iloc[6:16][['Time', column]].copy()

# # #             # Convertir los datos a formato numérico
# # #             df_filtered[column] = pd.to_numeric(df_filtered[column], errors='coerce')
# # #             df_filtered = df_filtered.rename(columns={column: 'Valor'})

# # #             # Crear la gráfica según el tipo seleccionado
# # #             if selected_chart == 'bar':
# # #                 fig = px.bar(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}',
# # #                              text='Valor')
# # #                 fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')

# # #             elif selected_chart == 'line':
# # #                 fig = px.line(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}',
# # #                               markers=True)

# # #             elif selected_chart == 'pie':
# # #                 fig = px.pie(df_filtered, values='Valor', names='Time', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'scatter':
# # #                 fig = px.scatter(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'area':
# # #                 fig = px.area(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'histogram':
# # #                 fig = px.histogram(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'box':
# # #                 fig = px.box(df_filtered, y='Valor', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'violin':
# # #                 fig = px.violin(df_filtered, y='Valor', title=f'{selected_time} {selected_line} {selected_category}')

# # #             elif selected_chart == 'heatmap':
# # #                 fig = px.density_heatmap(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}')
# # #             else:
# # #                 fig = px.bar(df_filtered, x='Time', y='Valor', title=f'{selected_time} {selected_line} {selected_category}')
# # #                 fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')

# # #             # Ajustar el rango del eje Y para mejorar la visualización
# # #             fig.update_layout(yaxis=dict(range=[0, df_filtered['Valor'].max() * 1.1]))
# # #         else:
# # #             fig = px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}')
# # #     else:
# # #         fig = px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}')

# # #     return fig
# # # #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# # import pandas as pd
# # import plotly.express as px
# # from dash import dcc, html, Input, Output, callback
# # import dash

# # # Enlace CSV de Google Sheets actualizado
# # CSV_URL = 'Carro Tensor  (3).xlsx'

# # # Función para obtener los datos desde el archivo Excel cargado
# # def obtener_datos_desde_csv():
# #     try:
# #         df = pd.read_excel(CSV_URL, sheet_name='RESUMEN CARRO TENSOR')
# #         return df
# #     except Exception as e:
# #         print(f"Error al obtener datos desde CSV: {e}")
# #         return pd.DataFrame()

# # # Definir las opciones de periodo, línea y categoría
# # time_options = ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']
# # line_options = ['LINEA ROJA', 'LINEA AMARILLA', 'LINEA VERDE', 'LINEA AZUL', 'LINEA PLATEADA']
# # category_options = ['S1R1', 'S2R1', 'S2R2', 'S1R2']

# # # Mapeo de columnas para cada combinación de línea y categoría por periodo
# # column_map = {
# #     'MENSUAL 05': {
# #         'LINEA ROJA': {'S1R1': 'MENSUSAL 05 ROJA S1R1', 'S2R1': 'MENSUSAL 05 ROJA S2R1'},
# #         # Puedes agregar más columnas aquí según necesites
# #     },
# #     # Agregar más periodos y líneas según tu archivo
# # }

# # # Layout de la aplicación
# # layout = html.Div([
# #     html.H1('Dashboard de Carro Tensor'),

# #     html.Div([
# #         html.Label('Seleccione el periodo:'),
# #         dcc.Dropdown(
# #             id='tiempo-dropdown',
# #             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
# #             value='MENSUAL 05'  # Valor predeterminado
# #         ),
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
# #     html.Div([
# #         html.Label('Seleccione la línea:'),
# #         dcc.Dropdown(
# #             id='linea-dropdown',
# #             options=[{'label': linea, 'value': linea} for linea in line_options],
# #             value='LINEA ROJA'  # Valor predeterminado
# #         ),
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# #     html.Div([
# #         html.Label('Seleccione la categoría:'),
# #         dcc.Dropdown(
# #             id='categoria-dropdown',
# #             options=[{'label': categoria, 'value': categoria} for categoria in category_options],
# #             value='S1R1'  # Valor predeterminado
# #         ),
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
# #     html.Br(),  # Añadir separación visual

# #     html.Div([
# #         dcc.Graph(id='dashboard-con')
# #     ], style={
# #         'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
# #         'padding': '20px',  # Añadir padding para mejor visualización
# #         'border-radius': '10px',  # Añadir bordes redondeados
# #         'marginBottom': '50px'
# #     }),

# #     html.Div([
# #         dcc.Graph(id='dashboard-sin')
# #     ], style={
# #         'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
# #         'padding': '20px',  # Añadir padding para mejor visualización
# #         'border-radius': '10px'
# #     })
# # ])

# # # Callback para actualizar ambos gráficos basado en la selección de periodo, línea y categoría
# # @callback(
# #     [Output('dashboard-con', 'figure'),
# #      Output('dashboard-sin', 'figure')],
# #     [Input('tiempo-dropdown', 'value'),
# #      Input('linea-dropdown', 'value'),
# #      Input('categoria-dropdown', 'value')]
# # )
# # def update_dashboards(selected_time, selected_line, selected_category):
# #     # Obtener los datos desde el archivo Excel
# #     df = obtener_datos_desde_csv()

# #     # Verificar si la selección existe en el mapa de columnas
# #     if selected_time in column_map and selected_line in column_map[selected_time]:
# #         column = column_map[selected_time][selected_line].get(selected_category, None)

# #         if column:
# #             # Filtrar los datos de las filas con "CON" en la columna "Tareas"
# #             df_con = df[df['Tareas'].str.contains('CON')][['Unnamed: 1', column]].copy()
# #             df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
# #             df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

# #             # Filtrar los datos de las filas con "SIN" en la columna "Tareas"
# #             df_sin = df[df['Tareas'].str.contains('SIN')][['Unnamed: 1', column]].copy()
# #             df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
# #             df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

# #             # Crear gráfica para "CON"
# #             fig_con = px.bar(df_con, x='Descripción', y='Valor', title=f'CON {selected_category}')
# #             fig_con.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# #             # Crear gráfica para "SIN"
# #             fig_sin = px.bar(df_sin, x='Descripción', y='Valor', title=f'SIN {selected_category}')
# #             fig_sin.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# #             return fig_con, fig_sin
# #         else:
# #             # Si no hay columnas válidas, devolver gráficos vacíos
# #             return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}'), \
# #                    px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}')
# #     else:
# #         # Si no se encuentra el mapeo adecuado
# #         return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}'), \
# #                px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}')
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash

# # URL del CSV de Google Sheets
# CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQeyBubLucOlpCdHKSjPNdQtdxI89y8nxyJH3o-rYnHmSwFrezuzFIfmmcwnUuvLb66PvZ2TJjCyzgg/pub?output=csv'

# # Función para obtener los datos desde el archivo CSV
# def obtener_datos_desde_csv():
#     try:
#         df = pd.read_csv(CSV_URL)
#         return df
#     except Exception as e:
#         print(f"Error al obtener datos desde CSV: {e}")
#         return pd.DataFrame()

# # Definir las opciones de periodo, línea y categoría
# time_options = ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']
# line_options = ['LINEA ROJA', 'LINEA AMARILLA', 'LINEA VERDE', 'LINEA AZUL', 'LINEA PLATEADA']
# category_options = ['S1R1', 'S2R1', 'S2R2', 'S1R2']

# # Mapeo de columnas para cada combinación de línea y categoría por periodo
# column_map = {
#     'MENSUAL 05': {
#         'LINEA ROJA': {'S1R1': 'MENSUSAL 05 ROJA S1R1', 'S2R1': 'MENSUSAL 05 ROJA S2R1'},
#         # Puedes agregar más columnas aquí según necesites
#     },
#     # Agregar más periodos y líneas según tu archivo
# }

# # Definir las opciones de tipo de gráfico
# graph_type_options = ['Barra', 'Línea', 'Dispersión']

# # Layout de la aplicación con un menú para el tipo de gráfico
# layout = html.Div([
#     html.H1('Dashboard de Carro Tensor'),

#     html.Div([
#         html.Label('Seleccione el periodo:'),
#         dcc.Dropdown(
#             id='tiempo-dropdown',
#             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
#             value='MENSUAL 05'  # Valor predeterminado
#         ),
#     ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
#     html.Div([
#         html.Label('Seleccione la línea:'),
#         dcc.Dropdown(
#             id='linea-dropdown',
#             options=[{'label': linea, 'value': linea} for linea in line_options],
#             value='LINEA ROJA'  # Valor predeterminado
#         ),
#     ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione la categoría:'),
#         dcc.Dropdown(
#             id='categoria-dropdown',
#             options=[{'label': categoria, 'value': categoria} for categoria in category_options],
#             value='S1R1'  # Valor predeterminado
#         ),
#     ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione el tipo de gráfico:'),
#         dcc.Dropdown(
#             id='tipo-grafico-dropdown',
#             options=[{'label': tipo, 'value': tipo} for tipo in graph_type_options],
#             value='Barra'  # Valor predeterminado
#         ),
#     ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Br(),  # Añadir separación visual

#     html.Div([
#         dcc.Graph(id='dashboard-con')
#     ], style={
#         'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
#         'padding': '20px',  # Añadir padding para mejor visualización
#         'border-radius': '10px',  # Añadir bordes redondeados
#         'marginBottom': '50px'
#     }),

#     html.Div([
#         dcc.Graph(id='dashboard-sin')
#     ], style={
#         'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
#         'padding': '20px',  # Añadir padding para mejor visualización
#         'border-radius': '10px'
#     })
# ])

# # Callback para actualizar ambos gráficos basado en la selección de periodo, línea, categoría y tipo de gráfico
# @callback(
#     [Output('dashboard-con', 'figure'),
#      Output('dashboard-sin', 'figure')],
#     [Input('tiempo-dropdown', 'value'),
#      Input('linea-dropdown', 'value'),
#      Input('categoria-dropdown', 'value'),
#      Input('tipo-grafico-dropdown', 'value')]
# )
# def update_dashboards(selected_time, selected_line, selected_category, selected_graph_type):
#     # Obtener los datos desde el archivo CSV
#     df = obtener_datos_desde_csv()

#     # Definir los colores basados en la línea seleccionada
#     line_colors = {
#         'LINEA ROJA': 'red',
#         'LINEA AMARILLA': 'yellow',
#         'LINEA VERDE': 'green',
#         'LINEA AZUL': 'blue',
#         'LINEA PLATEADA': 'gray'
#     }
    
#     color = line_colors.get(selected_line, 'black')  # Color predeterminado negro si no coincide

#     # Verificar si la selección existe en el mapa de columnas
#     if selected_time in column_map and selected_line in column_map[selected_time]:
#         column = column_map[selected_time][selected_line].get(selected_category, None)

#         if column:
#             # Filtrar los datos de las filas con "CON" en la columna "Tareas"
#             df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
#             df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
#             df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

#             # Filtrar los datos de las filas con "SIN" en la columna "Tareas"
#             df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
#             df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
#             df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

#             # Seleccionar el tipo de gráfico
#             if selected_graph_type == 'Barra':
#                 fig_con = px.bar(df_con, x='Descripción', y='Valor', title=f'CON {selected_category}', color_discrete_sequence=[color])
#                 fig_sin = px.bar(df_sin, x='Descripción', y='Valor', title=f'SIN {selected_category}', color_discrete_sequence=[color])
#             elif selected_graph_type == 'Línea':
#                 fig_con = px.line(df_con, x='Descripción', y='Valor', title=f'CON {selected_category}', line_shape='linear', color_discrete_sequence=[color])
#                 fig_sin = px.line(df_sin, x='Descripción', y='Valor', title=f'SIN {selected_category}', line_shape='linear', color_discrete_sequence=[color])
#             elif selected_graph_type == 'Dispersión':
#                 fig_con = px.scatter(df_con, x='Descripción', y='Valor', title=f'CON {selected_category}', color_discrete_sequence=[color])
#                 fig_sin = px.scatter(df_sin, x='Descripción', y='Valor', title=f'SIN {selected_category}', color_discrete_sequence=[color])

#             # Agregar texto en cada gráfico
#             fig_con.update_traces(texttemplate='%{y:.2f}', textposition='outside')
#             fig_sin.update_traces(texttemplate='%{y:.2f}', textposition='outside')

#             return fig_con, fig_sin
#         else:
#             # Si no hay columnas válidas, devolver gráficos vacíos

#             return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}'), \
#                    px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}')
#     else:
#         # Si no se encuentra el mapeo adecuado
#         return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}'), \
#                px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}')


import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# URL del CSV de Google Sheets
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQeyBubLucOlpCdHKSjPNdQtdxI89y8nxyJH3o-rYnHmSwFrezuzFIfmmcwnUuvLb66PvZ2TJjCyzgg/pub?output=csv'
           
# Función para obtener los datos desde el archivo CSV
def obtener_datos_desde_csv():
    try:
        df = pd.read_csv(CSV_URL)
        print(df.head())
        return df
    except Exception as e:
        print(f"Error al obtener datos desde CSV: {e}")
        return pd.DataFrame()
    

# Definir las opciones de periodo, línea y categoría
time_options = ['MOSTRAR DATOS TODOS LOS MESES','MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']
line_options = ['LINEA ROJA', 'LINEA AMARILLA', 'LINEA VERDE', 'LINEA AZUL', 'LINEA NARANJA', 'LINEA BLANCA', 'LINEA CELESTE', 'LINEA MORADA', 'LINEA CAFE', 'LINEA PLATEADA']
category_options = ['S1R1', 'S2R1', 'S2R2', 'S1R2']

# Mapeo de columnas para cada combinación de línea y categoría por periodo
column_map = {
    'MENSUAL 05': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 05 ROJA S1R1', 'S2R1': 'MENSUAL 05 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 05 AMARILLA S1R1', 'S1R2': 'MENSUAL 05 AMARILLA S1R2', 'S2R1': 'MENSUAL 05 AMARILLA S2R1'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 05 VERDE S1R1', 'S2R1': 'MENSUAL 05 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 05 AZUL S1R1', 'S2R1': 'MENSUAL 05 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 05 NARANJA S1R1', 'S2R1': 'MENSUAL 05 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 05 BLANCA S1R1', 'S2R1': 'MENSUAL 05 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 05 CELESTE S1R1', 'S2R1': 'MENSUAL 05 CELESTE S2R1', 'S2R2': 'MENSUAL 05 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 05 MORADA S1R1', 'S2R1': 'MENSUAL 05 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 05 PLATEADA S1R1', 'S2R1': 'MENSUAL 05 PLATEADA S2R1'},

        # Agregar más columnas aquí según sea necesario
    },
     'MENSUAL 06': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 06 ROJA S1R1', 'S2R1': 'MENSUAL 06 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 06 AMARILLA S1R1', 'S1R2': 'MENSUAL 06 AMARILLA S1R2', 'S1R2': 'MENSUAL 06 AMARILLA S1R2'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 06 VERDE S1R1', 'S2R1': 'MENSUAL 06 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 06 AZUL S1R1', 'S2R1': 'MENSUAL 06 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 06 NARANJA S1R1', 'S2R1': 'MENSUAL 06 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 06 BLANCA S1R1', 'S2R1': 'MENSUAL 06 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 06 CELESTE S1R1', 'S2R1': 'MENSUAL 06 CELESTE S2R1', 'S2R2': 'MENSUAL 06 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 06 MORADA S1R1', 'S2R1': 'MENSUAL 06 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 06 PLATEADA S1R1', 'S2R1': 'MENSUAL 06 PLATEADA S2R1'},
    # Agregar más periodos y líneas según el archivo
},
'MENSUAL 07': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 07 ROJA S1R1', 'S2R1': 'MENSUAL 07 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 07 AMARILLA S1R1', 'S2R1': 'MENSUAL 07 AMARILLA S2R1', 'S1R2': 'MENSUAL 07 AMARILLA S1R2'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 07 VERDE S1R1', 'S2R1': 'MENSUAL 07 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 07 AZUL S1R1', 'S2R1': 'MENSUAL 07 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 07 NARANJA S1R1', 'S2R1': 'MENSUAL 07 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 07 BLANCA S1R1', 'S2R1': 'MENSUAL 07 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 07 CELESTE S1R1', 'S2R1': 'MENSUAL 07 CELESTE S2R1', 'S2R2': 'MENSUAL 07 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 07 MORADA S1R1', 'S2R1': 'MENSUAL 07 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 07 PLATEADA S1R1', 'S2R1': 'MENSUAL 07 PLATEADA S2R1'},
    # Agregar más periodos y líneas según el archivo
},
'MENSUAL 08': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 08 ROJA S1R1', 'S2R1': 'MENSUAL 08 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 08 AMARILLA S1R1', 'S2R1': 'MENSUAL 08 AMARILLA S2R1','S1R2': 'MENSUAL 08 AMARILLA S1R2'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 08 VERDE S1R1', 'S2R1': 'MENSUAL 08 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 08 AZUL S1R1', 'S2R1': 'MENSUAL 08 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 08 NARANJA S1R1', 'S2R1': 'MENSUAL 08 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 08 BLANCA S1R1', 'S2R1': 'MENSUAL 08 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 08 CELESTE S1R1', 'S2R1': 'MENSUAL 08 CELESTE S2R1', 'S2R2': 'MENSUAL 08 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 08 MORADA S1R1', 'S2R1': 'MENSUAL 08 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 08 PLATEADA S1R1', 'S2R1': 'MENSUAL 08 PLATEADA S2R1'},
    # Agregar más periodos y líneas según el archivo
},
'MENSUAL 09': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 09 ROJA S1R1', 'S2R1': 'MENSUAL 09 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 09 AMARILLA S1R1', 'S2R1': 'MENSUAL 09 AMARILLA S2R1','S1R2': 'MENSUAL 09 AMARILLA S1R2'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 09 VERDE S1R1', 'S2R1': 'MENSUAL 09 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 09 AZUL S1R1', 'S2R1': 'MENSUAL 09 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 09 NARANJA S1R1', 'S2R1': 'MENSUAL 09 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 09 BLANCA S1R1', 'S2R1': 'MENSUAL 09 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 09 CELESTE S1R1', 'S2R1': 'MENSUAL 09 CELESTE S2R1', 'S2R2': 'MENSUAL 09 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 09 MORADA S1R1', 'S2R1': 'MENSUAL 09 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 09 PLATEADA S1R1', 'S2R1': 'MENSUAL 09 PLATEADA S2R1'},
    # Agregar más periodos y líneas según el archivo
},
'MENSUAL 10': {
        'LINEA ROJA': {'S1R1': 'MENSUAL 10 ROJA S1R1', 'S2R1': 'MENSUAL 10 ROJA S2R1'},
        'LINEA AMARILLA': {'S1R1': 'MENSUAL 10 AMARILLA S1R1', 'S2R1': 'MENSUAL 10 AMARILLA S2R1', 'S1R2': 'MENSUAL 10 AMARILLA S1R2'},
        'LINEA VERDE': {'S1R1': 'MENSUAL 10 VERDE S1R1', 'S2R1': 'MENSUAL 10 VERDE S2R1'},
        'LINEA AZUL': {'S1R1': 'MENSUAL 10 AZUL S1R1', 'S2R1': 'MENSUAL 10 AZUL S2R1'},
        'LINEA NARANJA': {'S1R1': 'MENSUAL 10 NARANJA S1R1', 'S2R1': 'MENSUAL 10 NARANJA S2R1'},
        'LINEA BLANCA': {'S1R1': 'MENSUAL 10 BLANCA S1R1', 'S2R1': 'MENSUAL 10 BLANCA S2R1'},
        'LINEA CELESTE': {'S1R1': 'MENSUAL 10 CELESTE S1R1', 'S2R1': 'MENSUAL 10 CELESTE S2R1', 'S2R2': 'MENSUAL 10 CELESTE S2R2'},
        'LINEA MORADA': {'S1R1': 'MENSUAL 10 MORADA S1R1', 'S2R1': 'MENSUAL 10 MORADA S2R1'},
        'LINEA CAFE': {'S1R2': 'MENSUAL 06 CAFE S1R2'},
        'LINEA PLATEADA': {'S1R1': 'MENSUAL 10 PLATEADA S1R1', 'S2R1': 'MENSUAL 10 PLATEADA S2R1'},
    # Agregar más periodos y líneas según el archivo
},
}

# Definir las opciones de tipo de gráfico
graph_type_options = ['Barra', 'Línea', 'Dispersión']

# Layout de la aplicación
layout = html.Div([
    html.H1('Dashboard de Carro Tensor'),

    # Dropdowns de opciones
    html.Div([
        html.Label('Seleccione el periodo:'),
        dcc.Dropdown(
            id='tiempo-dropdown-1',
            options=[{'label': periodo, 'value': periodo} for periodo in time_options],
            value='MENSUAL 05'  # Valor predeterminado
        ),
    ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
    html.Div([
        html.Label('Seleccione la línea:'),
        dcc.Dropdown(
            id='linea-dropdown-1',
            options=[{'label': linea, 'value': linea} for linea in line_options],
            value='LINEA ROJA'  # Valor predeterminado
        ),
    ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Div([
        html.Label('Seleccione la categoría:'),
        dcc.Dropdown(
            id='categoria-dropdown-1',
            options=[{'label': categoria, 'value': categoria} for categoria in category_options],
            value='S1R1'  # Valor predeterminado
        ),
    ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Div([
        html.Label('Seleccione el tipo de gráfico:'),
        dcc.Dropdown(
            id='tipo-grafico-dropdown-1',
            options=[{'label': tipo, 'value': tipo} for tipo in graph_type_options],
            value='Barra'  # Valor predeterminado
        ),
    ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Br(),

    html.Div([
        dcc.Graph(id='dashboard-con-1')
    ], style={
        'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)', 
        'padding': '20px', 
        'border-radius': '10px', 
        'marginBottom': '50px'
    }),

    html.Div([
        dcc.Graph(id='dashboard-sin-1')
    ], style={
        'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)', 
        'padding': '20px', 
        'border-radius': '10px'
    })
    
    
])
html.Br(),
# Callback para actualizar ambos gráficos basado en la selección de periodo, línea, categoría y tipo de gráfico
@callback(
    [Output('dashboard-con-1', 'figure'),
     Output('dashboard-sin-1', 'figure')],
    [Input('tiempo-dropdown-1', 'value'),
     Input('linea-dropdown-1', 'value'),
     Input('categoria-dropdown-1', 'value'),
     Input('tipo-grafico-dropdown-1', 'value')]
)
def update_dashboards(selected_time, selected_line, selected_category, selected_graph_type):
    # Obtener los datos desde el archivo CSV
    df = obtener_datos_desde_csv()

    # Definir los colores basados en la línea seleccionada
    line_colors = {
        'LINEA ROJA': 'red',
        'LINEA AMARILLA': 'yellow',
        'LINEA VERDE': 'green',
        'LINEA AZUL': 'blue',
        'LINEA NARANJA': 'orange',
        'LINEA BLANCA': 'black',
        'LINEA CELESTE': 'cyan',
        'LINEA MORADA': 'purple',
        'LINEA CAFE': 'brown',
        'LINEA PLATEADA': 'gray'
    }
    color = line_colors.get(selected_line, 'black')  # Color predeterminado negro si no coincide
    # figure_size = (800, 800)  # Ajusta las dimensiones de la figura aquí
    # Si se selecciona "MOSTRAR DATOS TODOS LOS MESES"
        # Si se selecciona "MOSTRAR DATOS TODOS LOS MESES"
    if selected_time == 'MOSTRAR DATOS TODOS LOS MESES':
        df_con_combined = pd.DataFrame()
        df_sin_combined = pd.DataFrame()

        for month in ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']:
            if month in column_map and selected_line in column_map[month]:
                if selected_category in column_map[month][selected_line]:
                    column = column_map[month][selected_line].get(selected_category, None)

                    if column:
                        # Filtrar y preparar datos para "CON CABINAS"
                        df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
                        df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
                        df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                        df_con['Mes'] = month
                        df_con_combined = pd.concat([df_con_combined, df_con], ignore_index=True)

                        # Filtrar y preparar datos para "SIN CABINAS"
                        df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
                        df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
                        df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                        df_sin['Mes'] = month
                        df_sin_combined = pd.concat([df_sin_combined, df_sin], ignore_index=True)

        # Crear la figura para "CON CABINAS" con tipo de gráfico seleccionado
        if selected_graph_type == 'Barra':
            fig_con = px.bar(df_con_combined, x='Mes', y='Valor', color='Descripción', title='CON CABINAS - Todos los Meses',
                             color_discrete_sequence=[color], barmode='group', text='Valor')
        # Crear la figura para "CON CABINAS" con tipo de gráfico Línea (con puntos y valores)
        if selected_graph_type == 'Línea':
            fig_con = px.line(
            df_con_combined.groupby('Mes').sum().reset_index(),
            x='Mes', y='Valor', 
            title='CON CABINAS - Todos los Meses',
            line_shape='linear',
            markers=True,
            color_discrete_sequence=[color]
        )

        # Agregar etiquetas de valor en cada punto
            fig_con.update_traces(text=df_con_combined.groupby('Mes').sum()['Valor'].apply(lambda x: f'{x:.2f}'), textposition='top center')

            # Agregar línea de tendencia
            if len(df_con_combined) > 1:
                x_values = np.arange(len(df_con_combined['Mes'].unique()))
                z = np.polyfit(x_values, df_con_combined.groupby('Mes').sum()['Valor'], 1)
                p = np.poly1d(z)
                fig_con.add_scatter(x=df_con_combined['Mes'].unique(), y=p(x_values), mode='lines', name='Tendencia', line=dict(color='black'))
                 # Expandir el rango del eje X para dar más espacio
                fig_con.update_xaxes(range=[-0.5, len(df_con_combined['Mes'].unique()) - 0.5])
            elif selected_graph_type == 'Dispersión':
    # Gráfico de dispersión para "CON CABINAS"
                fig_con = px.scatter(df_con_combined.groupby('Mes').sum().reset_index(), x='Mes', y='Valor', title='CON CABINAS - Todos los Meses',
                         color_discrete_sequence=[color])

        # Crear la figura para "SIN CABINAS" con tipo de gráfico seleccionado
        if selected_graph_type == 'Barra':
            fig_sin = px.bar(df_sin_combined, x='Mes', y='Valor', color='Descripción', title='SIN CABINAS - Todos los Meses',
                             color_discrete_sequence=[color], barmode='group', text='Valor')
        # Crear la figura para "SIN CABINAS" con tipo de gráfico Línea (con puntos y valores)
        if selected_graph_type == 'Línea':
            fig_sin = px.line(
            df_sin_combined.groupby('Mes').sum().reset_index(),
            x='Mes', y='Valor', 
            title='SIN CABINAS - Todos los Meses',
            line_shape='linear',
            markers=True,
            color_discrete_sequence=[color]
        )

        # Agregar etiquetas de valor en cada punto
            fig_sin.update_traces(text=df_sin_combined.groupby('Mes').sum()['Valor'].apply(lambda x: f'{x:.2f}'), textposition='top center')

            # Agregar línea de tendencia
            if len(df_sin_combined) > 1:
                x_values_sin = np.arange(len(df_sin_combined['Mes'].unique()))
                z_sin = np.polyfit(x_values_sin, df_sin_combined.groupby('Mes').sum()['Valor'], 1)
                p_sin = np.poly1d(z_sin)
                fig_sin.add_scatter(x=df_sin_combined['Mes'].unique(), y=p_sin(x_values_sin), mode='lines', name='Tendencia', line=dict(color='black'))
                # Expandir el rango del eje X para dar más espacio
                fig_sin.update_xaxes(range=[-0.5, len(df_sin_combined['Mes'].unique()) - 0.5])
            elif selected_graph_type == 'Dispersión':fig_sin = px.scatter(df_sin_combined.groupby('Mes').sum().reset_index(), x='Mes', y='Valor', title='SIN CABINAS - Todos los Meses',
                         color_discrete_sequence=[color])
    
        return fig_con, fig_sin

    # Si se selecciona un mes específico
    else:
        if selected_line in column_map[selected_time]:
            column = column_map[selected_time][selected_line].get(selected_category, None)

            if column:
                # Filtrar datos para "CON"
                df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
                df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
                df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

                # Filtrar datos para "SIN"
                df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
                df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
                df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

                # Crear la figura para el gráfico CON
                if selected_graph_type == 'Barra':
                    fig_con = px.bar(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
                                     color_discrete_sequence=[color])
                elif selected_graph_type == 'Línea':
                    fig_con = px.line(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
                                      color_discrete_sequence=[color])
                    
                 #   Agregar línea de tendencia si hay suficientes datos
                    if len(df_con) > 1:  # Asegúrate de tener más de un punto de datos
                        x_values = np.arange(len(df_con))  # Crear un array de índices
                        z = np.polyfit(x_values, df_con['Valor'], 1)  # Ajustar una línea
                        p = np.poly1d(z)  # Crear una función polinómica
                        # Añadir la línea de tendencia al gráfico
                        fig_con.add_scatter(x=df_con['Descripción'], y=p(x_values), mode='lines', name='Tendencia', line=dict(color='black'))
                elif selected_graph_type == 'Dispersión':
                    fig_con = px.scatter(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
                                         color_discrete_sequence=[color])

                # Crear la figura para el gráfico SIN
                if selected_graph_type == 'Barra':
                    fig_sin = px.bar(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
                                     color_discrete_sequence=[color])
                elif selected_graph_type == 'Línea':
                    fig_sin = px.line(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
                                      color_discrete_sequence=[color])

                    # Agregar línea de tendencia si hay suficientes datos
                    if len(df_sin) > 1:  # Asegúrate de tener más de un punto de datos
                        x_values_sin = np.arange(len(df_sin))  # Crear un array de índices
                        z_sin = np.polyfit(x_values_sin, df_sin['Valor'], 1)  # Ajustar una línea
                        p_sin = np.poly1d(z_sin)  # Crear una función polinómica  
                        # Añadir la línea de tendencia al gráfico
                        fig_sin.add_scatter(x=df_sin['Descripción'], y=p_sin(x_values_sin), mode='lines', name='Tendencia', line=dict(color='black'))                  
                elif selected_graph_type == 'Dispersión':
                    fig_sin = px.scatter(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
                                         color_discrete_sequence=[color])
                # fig_sin.update_layout(width=figure_size[0], height=figure_size[1], margin=dict(l=40, r=40, t=40, b=40))
                # # Ajustar el tamaño de la gráfica
                # fig_con.update_layout(width=600, height=400, margin=dict(l=40, r=40, t=40, b=40))
                # fig_sin.update_layout(width=600, height=400, margin=dict(l=40, r=40, t=40, b=40))

                # Expandir el rango del eje X para dar más espacio a la tendencia
                fig_con.update_xaxes(range=[-0.5, len(df_con) - 0.5])
                fig_sin.update_xaxes(range=[-0.5, len(df_sin) - 0.5])

                return fig_con, fig_sin

    # Si no hay datos para graficar, devolver gráficos vacíos
    return px.Figure(), px.Figure()


# yopi  yopi 
# yopi

    # if selected_time == 'MOSTRAR DATOS TODOS LOS MESES':
    #     df_con_combined = pd.DataFrame()
    #     df_sin_combined = pd.DataFrame()
        
    #     for month in ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']:
    #         if month in column_map and selected_line in column_map[month]:
    #             column = column_map[month][selected_line].get(selected_category, None)
                
    #             if column:
    #                 # Filtrar datos para "CON"
    #                 df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
    #                 df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
    #                 df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
    #                 df_con['Mes'] = month  # Añadir columna para el mes
    #                 df_con_combined = pd.concat([df_con_combined, df_con], ignore_index=True)

    #                 # Filtrar datos para "SIN"
    #                 df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
    #                 df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
    #                 df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
    #                 df_sin['Mes'] = month  # Añadir columna para el mes
    #                 df_sin_combined = pd.concat([df_sin_combined, df_sin], ignore_index=True)

    #     # Crear la figura para el gráfico CON
    #     if selected_graph_type == 'Barra':
    #         fig_con = px.bar(df_con_combined, x='Descripción', y='Valor', color='Mes', title='CON CABINAS - Todos los Meses',
    #                          color_discrete_sequence=px.colors.qualitative.Set1, barmode='group')
    #     elif selected_graph_type == 'Línea':
    #         fig_con = px.line(df_con_combined, x='Descripción', y='Valor', color='Mes', title='CON CABINAS - Todos los Meses',
    #                           color_discrete_sequence=px.colors.qualitative.Set1)
    #                     # Agregar línea de tendencia
    #         x_values = np.arange(len(df_con_combined))  # Crear un array de índices
    #         z = np.polyfit(x_values, df_con_combined['Valor'], 1)  # Ajustar una línea
    #         p = np.poly1d(z)  # Crear una función polinómica
    #         # Añadir la línea de tendencia al gráfico
    #         fig_con.add_scatter(x=df_con['Descripción'], y=p(x_values), mode='lines', name='Tendencia', line=dict(color='red'))
    #     elif selected_graph_type == 'Dispersión':
    #         fig_con = px.scatter(df_con_combined, x='Descripción', y='Valor', color='Mes', title='CON CABINAS - Todos los Meses',
    #                              color_discrete_sequence=px.colors.qualitative.Set1)

    #     # Crear la figura para el gráfico SIN
    #     if selected_graph_type == 'Barra':
    #         fig_sin = px.bar(df_sin_combined, x='Descripción', y='Valor', color='Mes', title='SIN CABINAS - Todos los Meses',
    #                          color_discrete_sequence=px.colors.qualitative.Set1, barmode='group')
    #     elif selected_graph_type == 'Línea':
    #         fig_sin = px.line(df_sin_combined, x='Descripción', y='Valor', color='Mes', title='SIN CABINAS - Todos los Meses',
    #                           color_discrete_sequence=px.colors.qualitative.Set1)
    #                     # Agregar línea de tendencia
    #         x_values_sin = np.arange(len(df_sin_combined))  # Crear un array de índices
    #         z_sin = np.polyfit(x_values_sin, df_sin_combined['Valor'], 1)  # Ajustar una línea
    #         p_sin = np.poly1d(z_sin)  # Crear una función polinómica
    #         # Añadir la línea de tendencia al gráfico
    #         fig_sin.add_scatter(x=df_sin['Descripción'], y=p_sin(x_values_sin), mode='lines', name='Tendencia', line=dict(color='red'))
                              
    #     elif selected_graph_type == 'Dispersión':
    #         fig_sin = px.scatter(df_sin_combined, x='Descripción', y='Valor', color='Mes', title='SIN CABINAS - Todos los Meses',
    #                              color_discrete_sequence=px.colors.qualitative.Set1)

    #     return fig_con, fig_sin

    # # Si se selecciona un mes específico
    # else:
    #     if selected_line in column_map[selected_time]:
    #         column = column_map[selected_time][selected_line].get(selected_category, None)

    #         if column:
    #             # Filtrar datos para "CON"
    #             df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
    #             df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
    #             df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

    #             # Filtrar datos para "SIN"
    #             df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
    #             df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
    #             df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

    #             # Crear la figura para el gráfico CON
    #             if selected_graph_type == 'Barra':
    #                 fig_con = px.bar(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
    #                                  color_discrete_sequence=[color])
    #             elif selected_graph_type == 'Línea':
    #                 fig_con = px.line(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
    #                                   color_discrete_sequence=[color])
    #                             # Agregar línea de tendencia
    #                 x_values = np.arange(len(df_con_combined))  # Crear un array de índices
    #                 z = np.polyfit(x_values, df_con_combined['Valor'], 1)  # Ajustar una línea
    #                 p = np.poly1d(z)  # Crear una función polinómica
    #                 # Añadir la línea de tendencia al gráfico
    #                 fig_con.add_scatter(x=df_con['Descripción'], y=p(x_values), mode='lines', name='Tendencia', line=dict(color='red'))
    #             elif selected_graph_type == 'Dispersión':
    #                 fig_con = px.scatter(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category} - {selected_time}',
    #                                      color_discrete_sequence=[color])

    #             # Crear la figura para el gráfico SIN
    #             if selected_graph_type == 'Barra':
    #                 fig_sin = px.bar(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
    #                                  color_discrete_sequence=[color])
    #             elif selected_graph_type == 'Línea':
    #                 fig_sin = px.line(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
    #                                   color_discrete_sequence=[color])
    #         # Agregar línea de tendencia
    #                 x_values_sin = np.arange(len(df_sin_combined))  # Crear un array de índices
    #                 z_sin = np.polyfit(x_values_sin, df_sin_combined['Valor'], 1)  # Ajustar una línea
    #                 p_sin = np.poly1d(z_sin)  # Crear una función polinómica  
    #                 # Añadir la línea de tendencia al gráfico
    #                 fig_sin.add_scatter(x=df_sin['Descripción'], y=p_sin(x_values_sin), mode='lines', name='Tendencia', line=dict(color='red'))                  
    #             elif selected_graph_type == 'Dispersión':
    #                 fig_sin = px.scatter(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category} - {selected_time}',
    #                                      color_discrete_sequence=[color])

    #             return fig_con, fig_sin

    # # Si no hay datos para graficar, devolver gráficos vacíos
    #         return px.Figure(), px.Figure()
    #     else:
    #         # Si no hay columnas válidas, devolver gráficos vacíos
    #      return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}'), \
    #                px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}')




# #     if selected_time == 'MOSTRAR DATOS TODOS LOS MESES':
#         figures_con = []
#         figures_sin = []
        
#         for month in ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']:
#             if month in column_map and selected_line in column_map[month]:
#                 column = column_map[month][selected_line].get(selected_category, None)
                
#                 if column:
#                     df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
#                     df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
#                     df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                    
#                     df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
#                     df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
#                     df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                    
#             # Imprimir valores para depuración
#             print(f"Tipo de gráfico seleccionado: {selected_graph_type}")
#             print(f"Categoría seleccionada: {selected_category}")
#             print(f"Color seleccionado: {color}")
#             print(f"Datos CON CABINAS: {df_con.head()}")
#             print(f"Datos SIN CABINAS: {df_sin.head()}")
#             print(df.columns)  # Verifica los nombres de las columnas


#              # Selección del tipo de gráfico
#             if selected_graph_type == 'Barra':
#               fig_con = px.bar(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category}', color_discrete_sequence=[color])
#               fig_sin = px.bar(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category}', color_discrete_sequence=[color])
     
#     # Ajustes específicos para gráficos de barra
#               fig_con.update_traces(texttemplate='%{y:.2f}', textposition='outside')
#               fig_sin.update_traces(texttemplate='%{y:.2f}', textposition='outside')

            # elif selected_graph_type == 'Línea':
            #   fig_con = px.line(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category}', line_shape='linear', color_discrete_sequence=[color])
            #   fig_sin = px.line(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category}', line_shape='linear', color_discrete_sequence=[color])
    
#     # Ajustes específicos para gráficos de línea (opcional)
#               fig_con.update_traces(mode='lines+markers')  # Mostrar líneas con marcadores
#               fig_sin.update_traces(mode='lines+markers')

#             elif selected_graph_type == 'Dispersión':
#              fig_con = px.scatter(df_con, x='Descripción', y='Valor', title=f'CON CABINAS {selected_category}', color_discrete_sequence=[color])
#              fig_sin = px.scatter(df_sin, x='Descripción', y='Valor', title=f'SIN CABINAS {selected_category}', color_discrete_sequence=[color])
    
#     # Ajustes específicos para gráficos de dispersión (opcional)
#              fig_con.update_traces(marker=dict(size=15))  # Cambiar tamaño de los puntos
#              fig_sin.update_traces(marker=dict(size=15))

#             else:
#                  print("Tipo de gráfico no reconocido")

# # Mostrar las gráficas
#             return fig_con, fig_sin

#         else:
#             # Si no hay columnas válidas, devolver gráficos vacíos
#             return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}'), \
#                    px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line} {selected_category}')
#     else:
#         # Si no se encuentra el mapeo adecuado
#         return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}'), \
#                px.bar(title=f'Sin datos disponibles para {selected_time} {selected_line}')
#------------------------------------------------------------------