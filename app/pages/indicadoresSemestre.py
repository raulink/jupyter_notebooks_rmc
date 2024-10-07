# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash

# # Enlace CSV de Google Sheets
# CSV_URL = 'https://docs.google.com/spreadsheets/d/1KdAnEDH4_lv6UMnUB_diVn3MFQdoYvEGE0LQcxXZ1-Y/pub?gid=0&single=true&output=csv'

# # Función para obtener los datos desde el enlace CSV de Google Sheets
# def obtener_datos_desde_csv(rango):
#     try:
#         # Leer los datos completos desde el CSV
#         df = pd.read_csv(CSV_URL, header=None)

#         # Convertir las filas y columnas a índices numéricos (empezando desde 0)
#         inicio_fila, fin_fila = rango['filas']
#         inicio_columna, fin_columna = rango['columnas']

#         # Seleccionar el rango específico
#         df_rango = df.iloc[inicio_fila:fin_fila, inicio_columna:fin_columna]

#         # Reiniciar los índices y establecer la primera fila como encabezados
#         df_rango.reset_index(drop=True, inplace=True)
#         df_rango.columns = df_rango.iloc[0]
#         df_rango = df_rango[1:]

#         return df_rango
#     except Exception as e:
#         print(f"Error al obtener datos desde CSV: {e}")
#         return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

# # Función para convertir los datos de porcentajes de texto a números
# def convertir_porcentajes(df):
#     if not df.empty:
#         for col in df.columns:
#             df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace(',', '.').str.strip(), errors='coerce')
#     return df

# # Definir las opciones de tiempo
# time_options = ['Semanales', 'Mensuales', 'Bimensuales', 'Trimestrales', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# # Asignar colores de forma dinámica para cada periodo y categoría
# categorias_base = ['AMARILLO', 'ROJA', 'AZUL', 'CELESTE', 'VERDE', 'BLANCO', 'NARANJA',
#                    'PLATEADA', 'MORADAS1', 'MORADAS2', 'CAFE']
# colores_base = ['yellow', 'red', 'blue', 'lightblue', 'green', 'white', 'orange',
#                 'silver', 'purple', 'purple', 'brown']
# periodos = ['Semanales', 'Mensuales', 'Bimensuales', 'Trimestrales', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# # Crear el diccionario de colores
# color_dict = {f'{periodo} {categoria}': color for periodo in periodos for categoria, color in zip(categorias_base, colores_base)}

# # Layout de la aplicación
# layout = html.Div([
#     html.H1('DASHBOARD DE INDICADORES POR SEMESTTRES'),
# html.Div([
#     html.Label('Seleccione el rango de fechas:'),
#     dcc.Dropdown(
#         id='fecha-dropdown',
#         options=[
#             {'label': 'Enero 2024', 'value': '2024-01'},
#             {'label': 'Febrero 2024', 'value': '2024-02'},
#             {'label': 'Marzo 2024', 'value': '2024-03'},
#             # Agrega más opciones según tus necesidades de fechas
#         ],
#         value='2024-01'  # Valor predeterminado
#     )
# ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),


#     html.Div([
#         html.Label('Seleccione el periodo:'),
#         dcc.Dropdown(
#             id='tiempo-dropdown-4',
#             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
#             value='Semanales'
#         ),
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
# html.Div([
#     html.Label('Seleccione el tipo de gráfico:'),
#     dcc.Dropdown(
#         id='tipo-grafico-dropdown',
#         options=[
#             {'label': 'Barras', 'value': 'bar'},
#             {'label': 'Líneas', 'value': 'line'},
#             {'label': 'Torta', 'value': 'pie'}
#         ],
#         value='bar'
#     )
# ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione las categorías:'),
#         dcc.Checklist(
#             id='categoria-checklist-4',
#             options=[],
#             value=[],
#             inline=True,
#         )
#     ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

#     html.Div([
#         dcc.Graph(id='dashboard-4')
#     ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
# ])

# # Rangos de celdas para cada periodo (ajustados a índices de pandas)
# rangos_periodo = {
#     'Semanales': {'filas': (6, 8), 'columnas': (3, 14)},          # D7:N8
#     'Mensuales': {'filas': (6, 8), 'columnas': (16, 27)},       # Q7:AA8
#     'Bimensuales': {'filas': (6, 8), 'columnas': (29, 40)},      # AD7:AN8
#     'Trimestrales': {'filas': (6, 8), 'columnas': (42, 53)},  # AQ7:BA8
#     'BALANCÍN ELÉCTRICO': {'filas': (6, 8), 'columnas': (55, 66)}, # BD7:BN8
#     'ANUAL MECÁNICO': {'filas': (6, 8), 'columnas': (68, 79)},     # BQ7:CA8
#     'ANUAL ELÉCTRICO': {'filas': (6, 8), 'columnas': (81, 92)}     # CD7:CN8
# }
# fechas_por_periodo = {
#     'Semanales': [
#         {'label': 'Enero 2024', 'value': '2024-01'},
#         {'label': 'Febrero 2024', 'value': '2024-02'}
#     ],
#     'Mensuales': [
#         {'label': '29/07/2024', 'value': '2024-07-29'},
#         {'label': '05/08/2024', 'value': '2024-08-05'},
#         {'label': '12/08/2024', 'value': '2024-08-12'},
#         {'label': '19/08/2024', 'value': '2024-08-19'},
#         {'label': '26/08/2024', 'value': '2024-08-26'}
#     ],
#     'Bimensuales': [
#         {'label': 'Abril 2024', 'value': '2024-04'},
#         {'label': 'Julio 2024', 'value': '2024-07'}
#     ],
#     'Trimestrales': [
#         {'label': 'Mayo 2024', 'value': '2024-05'},
#         {'label': 'Junio 2024', 'value': '2024-06'}
#     ],
#     'BALANCÍN ELÉCTRICO': [
#         {'label': 'Septiembre 2024', 'value': '2024-09'},
#         {'label': 'Octubre 2024', 'value': '2024-10'}
#     ],
#     'ANUAL MECÁNICO': [
#         {'label': 'Noviembre 2024', 'value': '2024-11'}
#     ],
#     'ANUAL ELÉCTRICO': [
#         {'label': 'Diciembre 2024', 'value': '2024-12'}























        
#     ]
# }
# # Mapeo de fechas y sus correspondientes filas y columnas en el archivo CSV
# rango_fechas_columnas = {
#     'Semanales': {
#         '2024-01': {'filas': (6, 8), 'columnas': (3, 14)},  # C2:L2
#         '2024-02': {'filas': (2, 3), 'columnas': (2, 12)},  # C3:L3
#         '2024-03': {'filas': (3, 4), 'columnas': (2, 12)},  # C4:L4
#     },
#     'Mensuales': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     },
#     'Bimensuales': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     },
#     'Trimestrales': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     },
#     'BIMENSUAL': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     },
#     'BIMENSUAL': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     },
#     'BIMENSUAL': {
#         '2024-07-29': {'filas': (6, 7), 'columnas': (2, 12)},  # C7:L7
#         '2024-08-05': {'filas': (7, 8), 'columnas': (2, 12)},  # C8:L8
#         '2024-08-12': {'filas': (8, 9), 'columnas': (2, 12)},  # C9:L9
#         # Agrega más fechas según tus necesidades
#     }
    
#     # Agrega los mapeos para otros periodos como TRIMESTRAL, etc.
# }

# # Callback para actualizar el dropdown de fechas basado en el periodo seleccionado
# @callback(
#     Output('fecha-dropdown', 'options'),
#     [Input('tiempo-dropdown-4', 'value')]
# )
# def update_fecha_dropdown(selected_time):
#     # Obtener las fechas correspondientes al periodo seleccionado
#     fechas = fechas_por_periodo.get(selected_time, [])
#     return fechas

# # Callback para actualizar las opciones del checklist basado en la selección de tiempo
# @callback(
#     Output('categoria-checklist-4', 'options'),
#     [Input('tiempo-dropdown-4', 'value')]
# )
# def update_checklist(selected_time):
#     # Obtener los datos más recientes desde el CSV
#     df = convertir_porcentajes(obtener_datos_desde_csv(rangos_periodo.get(selected_time, {'filas': (0, 0), 'columnas': (0, 0)})))

#     if df.empty:
#         print(f"No hay datos para el periodo {selected_time}.")
#         return []

#     options = [{'label': col, 'value': col} for col in df.columns]
#     return options

# # Callback para actualizar el dashboard basado en la selección del tiempo y categorías
# @callback(
#     Output('dashboard-4', 'figure'),
#     [Input('tiempo-dropdown-4', 'value'),
#      Input('categoria-checklist-4', 'value'),
#      Input('fecha-dropdown', 'value')]
# )
# def update_dashboard(selected_time, selected_categories, fecha_seleccionada):
#     # Verifica si el tiempo seleccionado tiene un rango de fechas asociado
#     if selected_time in rango_fechas_columnas and fecha_seleccionada in rango_fechas_columnas[selected_time]:
#         # Obtener las filas y columnas correspondientes a la fecha seleccionada
#         rango_columnas = rango_fechas_columnas[selected_time][fecha_seleccionada]
#     else:
#         return px.bar(title='Sin datos disponibles')

#     # # Obtener los datos desde el CSV para ese rango de columnas
#     df = convertir_porcentajes(obtener_datos_desde_csv(rango_columnas))

#     if not df.empty:
#         if not selected_categories:
#             selected_categories = df.columns

#         try:
#             # Filtrar las categorías seleccionadas
#             fila_filtrada = df[selected_categories].iloc[0]

#             df_temp = pd.DataFrame({
#                 'Categoría': fila_filtrada.index,
#                 'Porcentaje': fila_filtrada.values
#             })

#             # Normalizar los nombres de las categorías
#             df_temp['Categoría'] = df_temp['Categoría'].str.strip().str.upper()

#             # Asignar colores basados en los nombres de las categorías
#             df_temp['Color'] = df_temp['Categoría'].map(lambda x: color_dict.get(x, 'gray'))

#             # Generar el gráfico basado en el tipo seleccionado
#             fig = px.bar(df_temp, x='Categoría', y='Porcentaje',
#                          labels={'Categoría': 'Categoría', 'Porcentaje': 'Porcentaje'},
#                          title=f'Indicadores para {selected_time} y fecha {fecha_seleccionada}',
#                          color='Categoría',
#                          color_discrete_map=color_dict
#                         )
#             fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
#             fig.update_layout(yaxis=dict(range=[0, 100]))
#         except Exception as e:
#             print(f"Error al crear el gráfico: {e}")
#             fig = px.bar(title='Error al crear el gráfico')
#     else:
#         fig = px.bar(title='Sin datos disponibles')

#     return fig
