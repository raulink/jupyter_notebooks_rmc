# # import pandas as pd
# # import plotly.express as px
# # from dash import dcc, html, Input, Output, callback
# # import dash

# # # Enlace CSV de Google Sheets actualizado
# # CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVLpTYBRtueFth1XLrSL2ooOpWmT1mPPZRsxhTUrPb96OpNO6iiGDJ_ND0FmCbCHoVl8jR2wKmdUS_/pub?output=csv'

# # # Función para obtener los datos desde el enlace CSV de Google Sheets
# # def obtener_datos_desde_csv(rango):
# #     try:
# #         # Leer los datos completos desde el CSV
# #         df = pd.read_csv(CSV_URL, header=None)

# #         # Siempre usamos la primera fila como encabezado
# #         headers = df.iloc[0, rango['columnas'][0]:rango['columnas'][1]].values

# #         # Seleccionar las filas correspondientes a la semana
# #         inicio_fila, fin_fila = rango['filas']
# #         inicio_columna, fin_columna = rango['columnas']

# #         # Seleccionar los datos de la semana específica
# #         df_rango = df.iloc[inicio_fila:fin_fila, inicio_columna:fin_columna]

# #         # Asignar los encabezados
# #         df_rango.columns = headers

# #         return df_rango
# #     except Exception as e:
# #         print(f"Error al obtener datos desde CSV: {e}")
# #         return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

# # # Función para convertir los datos de porcentajes de texto a números
# # def convertir_porcentajes(df):
# #     if not df.empty:
# #         for col in df.columns:
# #             df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace(',', '.').str.strip(), errors='coerce')
# #     return df

# # # Definir las opciones de tiempo
# # time_options = ['semanales', 'mensuales', 'bimensuales', 'trimestrales', 'semestral', 'anual']

# # # Asignar categorías base y colores
# # categorias_base = ['RO', 'AM', 'VE', 'AZ', 'NA', 'BL', 'CE', 'MO', 'CA', 'PL']
# # colores_base = ['red', 'yellow', 'green', 'blue', 'orange', 'white', 'lightblue', 'purple', 'brown', 'silver']

# # # Crear el diccionario de colores
# # color_dict = {f'SEMANALES{categoria}': color for categoria, color in zip(categorias_base, colores_base)}

# # # Layout de la aplicación
# # layout = html.Div([
# #     html.H1('Dashboard de Indicadores'),

# #     html.Div([
# #         html.Label('Seleccione el rango de fechas:'),
# #         dcc.Dropdown(
# #             id='fecha-dropdown',
# #             options=[],  # Se actualiza dinámicamente según el periodo
# #             value=None  # Sin valor predeterminado
# #         )
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
# #        html.Div([
# #         html.Label('Seleccione el periodo:'),
# #         dcc.Dropdown(
# #             id='tiempo-dropdown',
# #             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
# #             value='semanales'  # Valor predeterminado
# #         ),
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# #     html.Div([
# #         html.Label('Seleccione el tipo de gráfico:'),
# #         dcc.Dropdown(
# #             id='tipo-grafico-dropdown',
# #             options=[
# #                 {'label': 'Barras', 'value': 'bar'},
# #                 {'label': 'Líneas', 'value': 'line'},
# #                 {'label': 'Torta', 'value': 'pie'}
# #             ],
# #             value='bar'
# #         )
# #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# #     html.Div([
# #         html.Label('Seleccione las categorías:'),
# #         dcc.Checklist(
# #             id='categoria-checklist',
# #             options=[],
# #             value=[],
# #             inline=True,
# #         )
# #     ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

# #     html.Div([
# #         dcc.Graph(id='dashboard')
# #     ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
# # ])

# # # Rangos de celdas para cada semana o mes ajustado a pandas (múltiples filas)
# # rangos_semanales = {
# #     'semana_1.1': {'filas': (0, 1), 'columnas': (2, 12)},  # Semana 1 está en la fila 3
# #     'semana_1': {'filas': (1, 2), 'columnas': (2, 12)},  # Semana 1 está en la fila 3
# #     'semana_2': {'filas': (2, 3), 'columnas': (2, 12)},  # Semana 2 está en la fila 4
# #     'semana_3': {'filas': (3, 4), 'columnas': (2, 12)},  # Semana 3 está en la fila 5
# #     'semana_4': {'filas': (4, 5), 'columnas': (2, 12)},  # Semana 4 está en la fila 6
# #     'semana_5': {'filas': (6, 7), 'columnas': (2, 12)},  # Semana 5 está en la fila 7
# #     'semana_6': {'filas': (7, 8), 'columnas': (2, 12)},  # Semana 6 está en la fila 8
# #     'semana_7': {'filas': (8, 9), 'columnas': (2, 12)},  # Semana 7 está en la fila 9
# #     'semana_8': {'filas': (9, 10), 'columnas': (2, 12)}, # Semana 8 está en la fila 10
# #     # Puedes seguir agregando más semanas según los datos en tu hoja
# # }
# # rangos_mensuales = {
# #     'semana_1': {'filas': (0, 1), 'columnas': (14, 24)},  # Semana 1 está en la fila 3
# #     'semana_2': {'filas': (1, 2), 'columnas': (14, 24)},  # Semana 2 está en la fila 4
# #     'semana_3': {'filas': (2, 3), 'columnas': (14, 24)},  # Semana 3 está en la fila 5
# #     'semana_4': {'filas': (3, 4), 'columnas': (14, 24)},  # Semana 4 está en la fila 6
# #     'semana_5': {'filas': (4, 5), 'columnas': (14, 24)},  # Semana 5 está en la fila 7
# #     'semana_6': {'filas': (5, 6), 'columnas': (14, 24)},  # Semana 6 está en la fila 8
# #     'semana_7': {'filas': (6, 7), 'columnas': (14, 24)},  # Semana 7 está en la fila 9
# #     'semana_8': {'filas': (7, 8), 'columnas': (14, 24)}, # Semana 8 está en la fila 10
# #     # Puedes seguir agregando más semanas según los datos en tu hoja
# # }
# # rangos_Bimensuales = {
# #     'semana_1': {'filas': (0, 1), 'columnas': (26, 36)},  # Semana 1 está en la fila 3
# #     'semana_2': {'filas': (1, 2), 'columnas': (26, 36)},  # Semana 2 está en la fila 4
# #     'semana_3': {'filas': (2, 3), 'columnas': (26, 36)},  # Semana 3 está en la fila 5
# #     'semana_4': {'filas': (3, 4), 'columnas': (26, 36)},  # Semana 4 está en la fila 6
# #     'semana_5': {'filas': (4, 5), 'columnas': (26, 36)},  # Semana 5 está en la fila 7
# #     'semana_6': {'filas': (5, 6), 'columnas': (26, 36)},  # Semana 6 está en la fila 8
# #     'semana_7': {'filas': (6, 7), 'columnas': (26, 36)},  # Semana 7 está en la fila 9
# #     'semana_8': {'filas': (7, 8), 'columnas': (26, 36)}, # Semana 8 está en la fila 10
# #     # Puedes seguir agregando más semanas según los datos en tu hoja
# # }

# # # Callback para actualizar el dropdown de fechas basado en el periodo seleccionado
# # @callback(
# #     Output('fecha-dropdown', 'options'),
# #     [Input('tiempo-dropdown', 'value')]
# # )
# # def update_fecha_dropdown(selected_time):
# #     # Obtener las fechas correspondientes al periodo seleccionado
# #     if selected_time == 'semanales':
# #         fechas = [{'label': f'Semana {i}', 'value': f'semana_{i}'} for i in range(1, 9)]
# #     elif selected_time == 'mensuales':
# #         fechas = [{'label': f'{mes.capitalize()} 2024', 'value': f'{mes}_2024'} for mes in ['enero', 'febrero', 'marzo']]
# #     else:
# #         fechas = []
# #     return fechas

# # # Callback para actualizar las opciones del checklist basado en la selección de tiempo
# # @callback(
# #     Output('categoria-checklist', 'options'),
# #     [Input('tiempo-dropdown', 'value'), Input('fecha-dropdown', 'value')]
# # )
# # def update_checklist(selected_time, selected_fecha):
# #     # Obtener los datos más recientes desde el CSV
# #     if selected_time == 'semanales':
# #         df = convertir_porcentajes(obtener_datos_desde_csv(rangos_semanales.get(selected_fecha, {'filas': (0, 0), 'columnas': (0, 0)})))
# #     elif selected_time == 'mensuales':
# #         df = convertir_porcentajes(obtener_datos_desde_csv(rangos_mensuales.get(selected_fecha, {'filas': (0, 0), 'columnas': (0, 0)})))
# #     elif selected_time == 'Bimensual':
# #         df = convertir_porcentajes(obtener_datos_desde_csv(rangos_Bimensuales.get(selected_fecha, {'filas': (0, 0), 'columnas': (0, 0)})))
# #     if df.empty:
# #         print(f"No hay datos para {selected_fecha}.")
# #         return []

# #     options = [{'label': col, 'value': col} for col in df.columns]
# #     return options

# # # Callback para actualizar el dashboard basado en la selección del tiempo y categorías
# # @callback(
# #     Output('dashboard', 'figure'),
# #     [Input('tiempo-dropdown', 'value'),
# #      Input('categoria-checklist', 'value'),
# #      Input('fecha-dropdown', 'value')]
# # )
# # def update_dashboard(selected_time, selected_categories, fecha_seleccionada):
# #     # Obtener los datos desde el CSV para el rango correspondiente
# #     if selected_time == 'semanales':
# #         df = convertir_porcentajes(obtener_datos_desde_csv(rangos_semanales.get(fecha_seleccionada, {'filas': (0, 0), 'columnas': (0, 0)})))
# #     elif selected_time == 'mensuales':
# #         df = convertir_porcentajes(obtener_datos_desde_csv(rangos_mensuales.get(fecha_seleccionada, {'filas': (0, 0), 'columnas': (0, 0)})))

# #     if not df.empty:
# #         if not selected_categories:
# #             selected_categories = df.columns

# #         try:
# #             # Filtrar las categorías seleccionadas
# #             fila_filtrada = df[selected_categories].iloc[0]

# #             df_temp = pd.DataFrame({
# #                 'Categoría': fila_filtrada.index,
# #                 'Porcentaje': fila_filtrada.values
# #             })

# #             # Normalizar los nombres de las categorías
# #             df_temp['Categoría'] = df_temp['Categoría'].str.strip().str.upper()

# #             # Generar el gráfico
# #             fig = px.bar(df_temp, x='Categoría', y='Porcentaje',
# #                          labels={'Categoría': 'Categoría', 'Porcentaje': 'Porcentaje'},
# #                          title=f'Indicadores para {selected_time} y fecha {fecha_seleccionada}',
# #                          color='Categoría',
# #                          color_discrete_map=color_dict
# #                         )
# #             fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
# #             fig.update_layout(yaxis=dict(range=[0, 100]))
# #         except Exception as e:
# #             print(f"Error al crear el gráfico: {e}")
# #             fig = px.bar(title='Error al crear el gráfico')
# #     else:
# #         fig = px.bar(title='Sin datos disponibles')

# #     return fig
# # # import pandas as pd
# # # import plotly.express as px
# # # from dash import dcc, html, Input, Output, callback
# # # import dash

# # # # Enlace CSV de Google Sheets actualizado
# # # CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVLpTYBRtueFth1XLrSL2ooOpWmT1mPPZRsxhTUrPb96OpNO6iiGDJ_ND0FmCbCHoVl8jR2wKmdUS_/pub?output=csv'

# # # # Función para obtener los datos desde el enlace CSV de Google Sheets
# # # def obtener_datos_desde_csv():
# # #     try:
# # #         # Leer los datos completos desde el CSV
# # #         df = pd.read_csv(CSV_URL, header=0)
# # #         return df
# # #     except Exception as e:
# # #         print(f"Error al obtener datos desde CSV: {e}")
# # #         return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

# # # # Definir las opciones de tiempo
# # # time_options = ['semanales', 'mensuales', 'bimensuales']

# # # # Layout de la aplicación
# # # layout = html.Div([
# # #     html.H1('Dashboard de Indicadores'),

# # #     html.Div([
# # #         html.Label('Seleccione el periodo:'),
# # #         dcc.Dropdown(
# # #             id='tiempo-dropdown',
# # #             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
# # #             value='semanales'  # Valor predeterminado
# # #         ),
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# # #     html.Div([
# # #         html.Label('Seleccione el tipo de gráfico:'),
# # #         dcc.Dropdown(
# # #             id='tipo-grafico-dropdown',
# # #             options=[
# # #                 {'label': 'Barras', 'value': 'bar'},
# # #                 {'label': 'Líneas', 'value': 'line'}
# # #             ],
# # #             value='bar'
# # #         )
# # #     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

# # #     html.Div([
# # #         dcc.Graph(id='dashboard')
# # #     ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
# # # ])

# # # # Callback para actualizar el dashboard basado en la selección del tiempo
# # # @callback(
# # #     Output('dashboard', 'figure'),
# # #     [Input('tiempo-dropdown', 'value'),
# # #      Input('tipo-grafico-dropdown', 'value')]
# # # )
# # # def update_dashboard(selected_time, selected_chart):
# # #     # Obtener los datos desde el CSV
# # #     df = obtener_datos_desde_csv()

# # #     # Filtrar las columnas según el periodo seleccionado
# # #     if selected_time == 'semanales':
# # #         columnas = ['Time', 'Semanales RO', 'Semanales AM', 'Semanales VE', 'Semanales AZ', 'Semanales NA', 'Semanales BL', 'Semanales CE', 'Semanales MO', 'Semanales CA', 'Semanales PL']
# # #     elif selected_time == 'mensuales':
# # #         columnas = ['Time', 'Mensuales RO', 'Mensuales AM', 'Mensuales VE', 'Mensuales AZ', 'Mensuales NA', 'Mensuales BL', 'Mensuales CE', 'Mensuales MO', 'Mensuales CA', 'Mensuales PL']
# # #     elif selected_time == 'bimensuales':
# # #         columnas = ['Time', 'Bimensuales RO', 'Bimensuales AM', 'Bimensuales VE', 'Bimensuales AZ', 'Bimensuales NA', 'Bimensuales BL', 'Bimensuales CE', 'Bimensuales MO', 'Bimensuales CA', 'Bimensuales PL']
    
# # #     df_filtered = df[columnas].copy()

# # #     # Convertir los datos a formato numérico
# # #     for col in df_filtered.columns[1:]:
# # #         df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

# # #     # Preparar los datos para la gráfica
# # #     df_melted = df_filtered.melt(id_vars='Time', var_name='Categoría', value_name='Valor')

# # #     # Crear la gráfica según el tipo seleccionado
# # #     if selected_chart == 'bar':
# # #         fig = px.bar(df_melted, x='Time', y='Valor', color='Categoría', barmode='group', title=f'Indicadores {selected_time.capitalize()}')
# # #     else:
# # #         fig = px.line(df_melted, x='Time', y='Valor', color='Categoría', title=f'Indicadores {selected_time.capitalize()}')

# # #     return fig
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash

# Enlace CSV de Google Sheets actualizado
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVLpTYBRtueFth1XLrSL2ooOpWmT1mPPZRsxhTUrPb96OpNO6iiGDJ_ND0FmCbCHoVl8jR2wKmdUS_/pub?output=csv'

# Función para obtener los datos desde el enlace CSV de Google Sheets
def obtener_datos_desde_csv():
    try:
        # Leer los datos completos desde el CSV
        df = pd.read_csv(CSV_URL, header=0)
        return df
    except Exception as e:
        print(f"Error al obtener datos desde CSV: {e}")
        return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

# Definir las opciones de tiempo
time_options = ['semanales', 'mensuales', 'bimensuales','Trimestrales','Semestral','Anual']

# Definir las opciones de colores (categorías base)
color_options = ['RO', 'AM', 'VE', 'AZ', 'NA', 'BL', 'CE', 'MO', 'CA', 'PL']

# Mapeo de colores para las categorías
color_map = {
    'RO': 'red',
    'AM': 'yellow',
    'VE': 'green',
    'AZ': 'blue',
    'NA': 'orange',
    'BL': 'black',
    'CE': 'cyan',
    'MO': 'purple',
    'CA': 'brown',
    'PL': 'gray'
}
# Layout de la aplicación
layout = html.Div([
    html.H1('Dashboard De Indicadores Semestre'),

    html.Div([
        html.Label('Seleccione el periodo:'),
        dcc.Dropdown(
            id='tiempo-dropdown',
            options=[{'label': periodo.capitalize(), 'value': periodo} for periodo in time_options],
            value='semanales'  # Valor predeterminado
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
    html.Div([
        html.Label('Seleccione el color (categoría):'),
        dcc.Dropdown(
            id='color-dropdown',
            options=[{'label': color, 'value': color} for color in color_options],
            value='RO'  # Valor predeterminado
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
    html.Div([
        html.Label('Seleccione el tipo de gráfico:'),
        dcc.Dropdown(
            id='tipo-grafico-dropdown',
            options=[
                {'label': 'Barras', 'value': 'bar'},             # Gráfico de barras
                {'label': 'Líneas', 'value': 'line'},            # Gráfico de líneas
                {'label': 'Torta', 'value': 'pie'},              # Gráfico de torta (pie chart)
                {'label': 'Área', 'value': 'area'},              # Gráfico de área
                {'label': 'Dispersión', 'value': 'scatter'},     # Gráfico de dispersión (scatter plot)
                {'label': 'Histograma', 'value': 'histogram'},   # Histograma
                {'label': 'Cajas', 'value': 'box'},              # Gráfico de cajas (box plot)
                {'label': 'Violín', 'value': 'violin'},          # Gráfico de violín (violin plot)
                {'label': 'Heatmap', 'value': 'heatmap'}         # Mapa de calor (heatmap)
            ],
            value='bar'
        )
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    html.Br(),
 # Otro salto de línea para separar el gráfico
    html.Br(),
    html.Div([
        dcc.Graph(id='dashboard')
    ], 
    style={
        'background-image': 'linear-gradient(to right, #83a4d4, #b6fbff)',  # Fondo degradado
        'padding': '20px',  # Añadir padding para mejor visualización
        'border-radius': '10px'  # Añadir bordes redondeados
    })
])
# Callback para actualizar el dashboard basado en la selección del periodo, color, y tipo de gráfico
@callback(
    Output('dashboard', 'figure'),
    [Input('tiempo-dropdown', 'value'),
     Input('color-dropdown', 'value'),
     Input('tipo-grafico-dropdown', 'value')]
)
def update_dashboard(selected_time, selected_color, selected_chart):
    # Obtener los datos desde el CSV
    df = obtener_datos_desde_csv()

    # Definir las columnas según el periodo seleccionado
    columnas_por_periodo = {
        'semanales': {
            'RO': 'Semanales RO', 'AM': 'Semanales AM', 'VE': 'Semanales VE',
            'AZ': 'Semanales AZ', 'NA': 'Semanales NA', 'BL': 'Semanales BL',
            'CE': 'Semanales CE', 'MO': 'Semanales MO',
            'CA': 'Semanales CA', 'PL': 'Semanales PL'
        },
        'mensuales': {
            'RO': 'Mensuales RO', 'AM': 'Mensuales AM', 'VE': 'Mensuales VE',
            'AZ': 'Mensuales AZ', 'NA': 'Mensuales NA', 'BL': 'Mensuales BL',
            'CE': 'Mensuales CE', 'MO': 'Mensuales MO', 'CA': 'Mensuales CA', 'PL': 'Mensuales PL'
        },
        'bimensuales': {
            'RO': 'Bimensuales RO', 'AM': 'Bimensuales AM', 'VE': 'Bimensuales VE',
            'AZ': 'Bimensuales AZ', 'NA': 'Bimensuales NA', 'BL': 'Bimensuales BL',
            'CE': 'Bimensuales CE', 'MO': 'Bimensuales MO', 'CA': 'Bimensuales CA', 'PL': 'Bimensuales PL'
        },
        'Trimestrales': {
            'RO': 'Trimestrales RO', 'AM': 'Trimestrales AM', 'VE': 'Trimestrales VE',
            'AZ': 'Trimestrales AZ', 'NA': 'Trimestrales NA', 'BL': 'Trimestrales BL',
            'CE': 'Trimestrales CE', 'MO': 'Trimestrales MO', 'CA': 'Trimestrales CA', 'PL': 'Trimestrales PL'
        },
        'Semestral': {
            'RO': 'Semestral RO', 'AM': 'Semestral AM', 'VE': 'Semestral VE',
            'AZ': 'Semestral AZ', 'NA': 'Semestral NA', 'BL': 'Semestral BL',
            'CE': 'Semestral CE', 'MO': 'Semestral MO', 'CA': 'Semestral CA', 'PL': 'Semestral PL'
        },
        'Anual': {
            'RO': 'Anual RO', 'AM': 'Anual AM', 'VE': 'Anual VE',
            'AZ': 'Anual AZ', 'NA': 'Anual NA', 'BL': 'Anual BL',
            'CE': 'Anual CE', 'MO': 'Anual MO', 'CA': 'Anual CA', 'PL': 'Anual PL'
        }
    }

    # Filtrar los datos según el periodo y color seleccionado
    columna = columnas_por_periodo[selected_time].get(selected_color, None)
    if not columna:
        return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_color}')
    df_filtered = df[['Time', columna]].copy()
    # Convertir los datos a formato numérico
    df_filtered[columna] = pd.to_numeric(df_filtered[columna], errors='coerce')
    # Renombrar la columna a 'Valor' para estandarizar
    df_filtered = df_filtered.rename(columns={columna: 'Valor'})
    # Obtener el color correspondiente para las barras
    color_barras = color_map[selected_color]
    # Crear la gráfica según el tipo seleccionado
        # Crear la gráfica según el tipo seleccionado
    if selected_chart == 'bar':
        # Gráfico de barras con color personalizado
        fig = px.bar(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}',
                     text='Valor')
        fig.update_traces(marker_color=color_barras, texttemplate='%{y:.2f}%', textposition='outside')
        # Nuevo para gráfico de torta
    elif selected_chart == 'pie':
        fig = px.pie(df_filtered, values='Valor', names='Time', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para gráfico de área
    elif selected_chart == 'area':
        fig = px.area(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para gráfico de dispersión
    elif selected_chart == 'scatter':
        fig = px.scatter(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para histograma
    elif selected_chart == 'histogram':
        fig = px.histogram(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para gráfico de cajas (box plot)
    elif selected_chart == 'box':
        fig = px.box(df_filtered, y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para gráfico de violín (violin plot)
    elif selected_chart == 'violin':
        fig = px.violin(df_filtered, y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')

    # Nuevo para mapa de calor (heatmap)
    elif selected_chart == 'heatmap':
        fig = px.density_heatmap(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}')
    else:
        # Gráfico de líneas con color personalizado
        fig = px.line(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}',
                      markers=True, text='Valor')
        fig.update_traces(line_color=color_barras, texttemplate='%{y:.2f}%', textposition='top center')

    # Ajustar el rango del eje Y para mejorar la visualización
    fig.update_layout(yaxis=dict(range=[0, 1.1]))

    return fig

# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash

# # Enlace CSV de Google Sheets actualizado
# CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVLpTYBRtueFth1XLrSL2ooOpWmT1mPPZRsxhTUrPb96OpNO6iiGDJ_ND0FmCbCHoVl8jR2wKmdUS_/pub?output=csv'

# # Función para obtener los datos desde el enlace CSV de Google Sheets
# def obtener_datos_desde_csv():
#     try:
#         # Leer los datos completos desde el CSV
#         df = pd.read_csv(CSV_URL, header=0)
#         return df
#     except Exception as e:
#         print(f"Error al obtener datos desde CSV: {e}")
#         return pd.DataFrame()  # Retornar un DataFrame vacío en caso de error

# # Definir las opciones de tiempo
# time_options = ['semanales', 'mensuales', 'bimensuales']

# # Definir las opciones de colores (categorías base)
# color_options = ['RO', 'AM', 'VE', 'AZ', 'NA', 'BL', 'CE', 'MO', 'CA', 'PL']

# # Mapeo de colores para las categorías
# color_map = {
#     'RO': 'red',
#     'AM': 'yellow',
#     'VE': 'green',
#     'AZ': 'blue',
#     'NA': 'orange',
#     'BL': 'black',
#     'CE': 'cyan',
#     'MO': 'purple',
#     'CA': 'brown',
#     'PL': 'gray'
# }

# # Layout de la aplicación
# layout = html.Div([
#     html.H1('Dashboard de Indicadores'),

#     html.Div([
#         html.Label('Seleccione el periodo:'),
#         dcc.Dropdown(
#             id='tiempo-dropdown',
#             options=[{'label': periodo.capitalize(), 'value': periodo} for periodo in time_options],
#             value='semanales'  # Valor predeterminado
#         ),
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione el color (categoría):'),
#         dcc.Dropdown(
#             id='color-dropdown',
#             options=[{'label': color, 'value': color} for color in color_options],
#             value='RO'  # Valor predeterminado
#         ),
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione el tipo de gráfico:'),
#         dcc.Dropdown(
#             id='tipo-grafico-dropdown',
#             options=[
#                 {'label': 'Barras', 'value': 'bar'},
#                 {'label': 'Líneas', 'value': 'line'}
#             ],
#             value='bar'
#         )
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         dcc.Graph(id='dashboard')
#     ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
# ])

# # Callback para actualizar el dashboard basado en la selección del periodo, color, y tipo de gráfico
# @callback(
#     Output('dashboard', 'figure'),
#     [Input('tiempo-dropdown', 'value'),
#      Input('color-dropdown', 'value'),
#      Input('tipo-grafico-dropdown', 'value')]
# )
# def update_dashboard(selected_time, selected_color, selected_chart):
#     # Obtener los datos desde el CSV
#     df = obtener_datos_desde_csv()

#     # Definir las columnas según el periodo seleccionado
#     columnas_por_periodo = {
#         'semanales': {
#             'RO': 'Semanales RO', 'AM': 'Semanales AM', 'VE': 'Semanales VE',
#             'AZ': 'Semanales AZ', 'NA': 'Semanales NA', 'BL': 'Semanales BL',
#             'CE': 'Semanales CE', 'MO': 'Semanales MO',
#             'CA': 'Semanales CA', 'PL': 'Semanales PL'
#         },
#         'mensuales': {
#             'RO': 'Mensuales RO', 'AM': 'Mensuales AM', 'VE': 'Mensuales VE',
#             'AZ': 'Mensuales AZ', 'NA': 'Mensuales NA', 'BL': 'Mensuales BL',
#             'CE': 'Mensuales CE', 'MO': 'Mensuales MO', 'CA': 'Mensuales CA', 'PL': 'Mensuales PL'
#         },
#         'bimensuales': {
#             'RO': 'Bimensuales RO', 'AM': 'Bimensuales AM', 'VE': 'Bimensuales VE',
#             'AZ': 'Bimensuales AZ', 'NA': 'Bimensuales NA', 'BL': 'Bimensuales BL',
#             'CE': 'Bimensuales CE', 'MO': 'Bimensuales MO', 'CA': 'Bimensuales CA', 'PL': 'Bimensuales PL'
#         }
#     }

#     # Filtrar los datos según el periodo y color seleccionado
#     columna = columnas_por_periodo[selected_time].get(selected_color, None)

#     if not columna:
#         return px.bar(title=f'Sin datos disponibles para {selected_time} {selected_color}')

#     df_filtered = df[['Time', columna]].copy()

#     # Convertir los datos a formato numérico
#     df_filtered[columna] = pd.to_numeric(df_filtered[columna], errors='coerce')

#     # Renombrar la columna a 'Valor' para estandarizar
#     df_filtered = df_filtered.rename(columns={columna: 'Valor'})

#     # Obtener el color correspondiente para las barras
#     color_barras = color_map[selected_color]

#     # Crear la gráfica según el tipo seleccionado
#     if selected_chart == 'bar':
#         # Gráfico de barras con color personalizado
#         fig = px.bar(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}',
#                      text='Valor')
#         fig.update_traces(marker_color=color_barras, texttemplate='%{y:.2f}%', textposition='outside')
#     else:
#         # Gráfico de líneas con color personalizado
#         fig = px.line(df_filtered, x='Time', y='Valor', title=f'Indicadores {selected_time.capitalize()} {selected_color}',
#                       markers=True, text='Valor')
#         fig.update_traces(line_color=color_barras, texttemplate='%{y:.2f}%', textposition='top center')

#     # Ajustar el rango del eje Y para mejorar la visualización
#     fig.update_layout(yaxis=dict(range=[0, 1.1]))

#     return fig
