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
# time_options = ['MENSUAL', 'BIMENSUAL', 'TRIMESTRAL', 'BALANCÍN MECÁNICO', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# # Asignar colores de forma dinámica para cada periodo y categoría
# categorias_base = ['AMARILLO', 'ROJA', 'AZUL', 'CELESTE', 'VERDE', 'BLANCO', 'NARANJA',
#                    'PLATEADA', 'MORADAS1', 'MORADAS2', 'CAFE']
# colores_base = ['yellow', 'red', 'blue', 'lightblue', 'green', 'white', 'orange',
#                 'silver', 'purple', 'purple', 'brown']
# periodos = ['MENSUAL', 'BIMENSUAL', 'TRIMESTRAL', 'BALANCÍN MECÁNICO', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']


# # Crear el diccionario de colores
# color_dict = {f'{periodo} {categoria}': color for periodo in periodos for categoria, color in zip(categorias_base, colores_base)}

# # Layout de la aplicación
# layout = html.Div([
#     html.H1('DASHBOARD DE INDICADORES DE TORRES'),

#     html.Div([
#         html.Label('Seleccione el periodo:'),
#         dcc.Dropdown(
#             id='tiempo-dropdown-2',
#             options=[{'label': periodo, 'value': periodo} for periodo in time_options],
#             value='MENSUAL'
#         ),
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
    
#     # Nuevo menú desplegable para seleccionar el color
#     html.Div([
#         html.Label('Seleccione el color:'),
#         dcc.Dropdown(
#             id='color-dropdown',
#             options=[{'label': color, 'value': color} for color in categorias_base],
#             value=''  # Valor predeterminado
#         ),
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),
#     html.Div([
#         html.Label('Seleccione el tipo de gráfico:'),
#         dcc.Dropdown(
#             id='tipo-grafico-dropdown',
#             options=[
#                 {'label': 'Barras', 'value': 'bar'},             # Gráfico de barras
#                 {'label': 'Líneas', 'value': 'line'},            # Gráfico de líneas
#                 {'label': 'Torta', 'value': 'pie'},              # Gráfico de torta (pie chart)
#                 {'label': 'Área', 'value': 'area'},              # Gráfico de área
#                 {'label': 'Dispersión', 'value': 'scatter'},     # Gráfico de dispersión (scatter plot)
#                 {'label': 'Histograma', 'value': 'histogram'},   # Histograma
#                 {'label': 'Cajas', 'value': 'box'},              # Gráfico de cajas (box plot)
#                 {'label': 'Violín', 'value': 'violin'},          # Gráfico de violín (violin plot)
#                 {'label': 'Heatmap', 'value': 'heatmap'}         # Mapa de calor (heatmap)
#             ],
#             value='bar'
#         )
#     ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

#     html.Div([
#         html.Label('Seleccione las categorías:'),
#         dcc.Checklist(
#             id='categoria-checklist-2',
#             options=[],
#             value=[],
#             inline=True,
#         )
#     ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

#     html.Div([
#         dcc.Graph(id='dashboard-2')
#     ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
# ])


# # Rangos de celdas para cada periodo (ajustados a índices de pandas)
# rangos_periodo = {
#     'MENSUAL': {'filas': (6, 8), 'columnas': (3, 14)},          # D7:N8
#     'BIMENSUAL': {'filas': (6, 8), 'columnas': (16, 27)},       # Q7:AA8
#     'TRIMESTRAL': {'filas': (6, 8), 'columnas': (29, 40)},      # AD7:AN8
#     'BALANCÍN MECÁNICO': {'filas': (6, 8), 'columnas': (42, 53)},  # AQ7:BA8
#     'BALANCÍN ELÉCTRICO': {'filas': (6, 8), 'columnas': (55, 66)}, # BD7:BN8
#     'ANUAL MECÁNICO': {'filas': (6, 8), 'columnas': (68, 79)},     # BQ7:CA8
#     'ANUAL ELÉCTRICO': {'filas': (6, 8), 'columnas': (81, 92)}     # CD7:CN8
# }

# # Callback para actualizar las opciones del checklist basado en la selección de tiempo
# @callback(
#     Output('categoria-checklist-2', 'options'),
#     [Input('tiempo-dropdown-2', 'value')]
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
#     Output('dashboard-2', 'figure'),
#     [Input('tiempo-dropdown-2', 'value'),
#      Input('categoria-checklist-2', 'value')]
# )
# def update_dashboard(selected_time, selected_categories):
#     # Obtener los datos más recientes desde el CSV
#     df = convertir_porcentajes(obtener_datos_desde_csv(rangos_periodo.get(selected_time, {'filas': (0, 0), 'columnas': (0, 0)})))

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

#             # # Normalizar los nombres de las categorías para evitar discrepancias
#             df_temp['Categoría'] = df_temp['Categoría'].str.strip().str.upper()

#             # Asignar colores basados en los nombres de las categorías
#             df_temp['Color'] = df_temp['Categoría'].map(lambda x: color_dict.get(x, 'gray'))

#             fig = px.bar(df_temp, x='Categoría', y='Porcentaje',
#                          labels={'Categoría': 'Categoría', 'Porcentaje': 'Porcentaje'},
#                          title=f'Indicadores De Torres {selected_time}',
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

import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash

# Enlace CSV de Google Sheets
CSV_URL = 'https://docs.google.com/spreadsheets/d/1KdAnEDH4_lv6UMnUB_diVn3MFQdoYvEGE0LQcxXZ1-Y/pub?gid=0&single=true&output=csv'

# Función para obtener los datos desde el enlace CSV de Google Sheets
def obtener_datos_desde_csv(rango=None):
    try:
        df = pd.read_csv(CSV_URL, header=None)
        if rango:
            # Convertir las filas y columnas a índices numéricos (empezando desde 0)
            inicio_fila, fin_fila = rango['filas']
            inicio_columna, fin_columna = rango['columnas']
            # Seleccionar el rango específico
            df = df.iloc[inicio_fila:fin_fila, inicio_columna:fin_columna]
        # Reiniciar los índices y establecer la primera fila como encabezados
        df.reset_index(drop=True, inplace=True)
        df.columns = df.iloc[0]
        df = df[1:]
        return df
    except Exception as e:
        print(f"Error al obtener datos desde CSV: {e}")
        return pd.DataFrame()

# Función para convertir los datos de porcentajes de texto a números
def convertir_porcentajes(df):
    if not df.empty:
        for col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace(',', '.').str.strip(), errors='coerce')
    return df

# Definir las opciones de tiempo
time_options = ['MENSUAL', 'BIMENSUAL', 'TRIMESTRAL', 'BALANCÍN MECÁNICO', 'BALANCÍN ELÉCTRICO', 'ANUAL MECÁNICO', 'ANUAL ELÉCTRICO']

# Asignar colores de forma dinámica para cada periodo y categoría
categorias_base = ['AMARILLO', 'ROJA', 'AZUL', 'CELESTE', 'VERDE', 'BLANCO', 'NARANJA', 'PLATEADA', 'MORADAS1', 'MORADAS2', 'CAFE']
colores_base = ['yellow', 'red', 'blue', 'lightblue', 'green', 'white', 'orange', 'silver', 'purple', 'purple', 'brown']

# Crear el diccionario de colores
color_dict = {f'{categoria}': color for categoria, color in zip(categorias_base, colores_base)}

# Layout de la aplicación
layout = html.Div([
    html.H1('DASHBOARD DE INDICADORES DE TORRES  '),

    html.Div([
        html.Label('Seleccione el periodo:'),
        dcc.Dropdown(
            id='tiempo-dropdown-2',
            options=[{'label': periodo, 'value': periodo} for periodo in time_options],
            value='MENSUAL'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    # Nuevo menú desplegable para seleccionar el color
    html.Div([
        html.Label('Seleccione el color:'),
        dcc.Dropdown(
            id='color-dropdown',
            options=[{'label': color, 'value': color} for color in categorias_base],
            value=''  # Valor predeterminado
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Div([
        html.Label('Seleccione el tipo de gráfico:'),
        dcc.Dropdown(
            id='tipo-grafico-dropdown',
            options=[
                {'label': 'Barras', 'value': 'bar'},
                # {'label': 'Líneas', 'value': 'line'},
                {'label': 'Torta', 'value': 'pie'},
                # {'label': 'Área', 'value': 'area'},
                # {'label': 'Dispersión', 'value': 'scatter'},
                # {'label': 'Histograma', 'value': 'histogram'},
                # {'label': 'Cajas', 'value': 'box'},
                # {'label': 'Violín', 'value': 'violin'},
                # {'label': 'Heatmap', 'value': 'heatmap'}
            ],
            value='bar'
        )
    ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Div([
        html.Label('Seleccione las categorías:'),
        dcc.Checklist(
            id='categoria-checklist-2',
            options=[],
            value=[],
            inline=True,
        )
    ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='dashboard-2')
    ],     
    style={
        'background-image': 'linear-gradient(to right, #380B61, #BF00FF)',  # Fondo degradado
        'padding': '10px',  # Añadir padding para mejor visualización
        'border-radius': '10px'  # Añadir bordes redondeados
    })
])

# Rangos de celdas para cada periodo (ajustados a índices de pandas)
rangos_periodo = {
    'MENSUAL': {'filas': (6, 8), 'columnas': (3, 14)},
    'BIMENSUAL': {'filas': (6, 8), 'columnas': (16, 27)},
    'TRIMESTRAL': {'filas': (6, 8), 'columnas': (29, 40)},
    'BALANCÍN MECÁNICO': {'filas': (6, 8), 'columnas': (42, 53)},
    'BALANCÍN ELÉCTRICO': {'filas': (6, 8), 'columnas': (55, 66)},
    'ANUAL MECÁNICO': {'filas': (6, 8), 'columnas': (68, 79)},
    'ANUAL ELÉCTRICO': {'filas': (6, 8), 'columnas': (81, 92)}
}

# Callback para actualizar las opciones del checklist basado en la selección de tiempo
@callback(
    Output('categoria-checklist-2', 'options'),
    [Input('tiempo-dropdown-2', 'value')]
)
def update_checklist(selected_time):
    df = convertir_porcentajes(obtener_datos_desde_csv(rangos_periodo.get(selected_time, {'filas': (0, 0), 'columnas': (0, 0)})))

    if df.empty:
        return []

    options = [{'label': col, 'value': col} for col in df.columns]
    return options

# Callback para manejar la selección de color o período y actualizar el dashboard
@callback(
    Output('dashboard-2', 'figure'),
    [Input('tiempo-dropdown-2', 'value'),
     Input('color-dropdown', 'value'),
     Input('categoria-checklist-2', 'value'),
     Input('tipo-grafico-dropdown', 'value')]
)
def update_dashboard(selected_time, selected_color, selected_categories, selected_chart):
    df_combined = pd.DataFrame()

    if selected_color:
        # Graficar todos los periodos para un color específico
        for periodo in rangos_periodo.keys():
            df = convertir_porcentajes(obtener_datos_desde_csv(rangos_periodo.get(periodo, {'filas': (0, 0), 'columnas': (0, 0)})))
            if not df.empty:
                try:
                    fila_filtrada = df[[col for col in df.columns if selected_color.upper() in col.upper()]].iloc[0]
                    df_temp = pd.DataFrame({
                        'Periodo': [periodo],
                        'Porcentaje': [fila_filtrada.values[0]]
                    })
                    df_combined = pd.concat([df_combined, df_temp], ignore_index=True)
                except Exception as e:
                    print(f"Error al procesar los datos para {periodo}y el color {selected_color}: {e}")

        # Si hay datos para el color seleccionado, crear el gráfico
        if not df_combined.empty:
            if selected_chart == 'bar':
                fig = px.bar(df_combined, x='Periodo', y='Porcentaje', title=f'Indicadores para {selected_color}',
                             color_discrete_sequence=[color_dict[selected_color]], text='Porcentaje')
            elif selected_chart == 'line':
                fig = px.line(df_combined, x='Periodo', y='Porcentaje', title=f'Indicadores para {selected_color}',
                              color_discrete_sequence=[color_dict[selected_color]], markers=True)
            elif selected_chart == 'pie':
                fig = px.pie(df_combined, values='Porcentaje', names='Periodo', title=f'Indicadores para {selected_color}')
            elif selected_chart == 'scatter':
                fig = px.scatter(df_combined, x='Periodo', y='Porcentaje', title=f'Indicadores para {selected_color}',
                                 color_discrete_sequence=[color_dict[selected_color]])
            elif selected_chart == 'area':
                fig = px.area(df_combined, x='Periodo', y='Porcentaje', title=f'Indicadores para {selected_color}',
                              color_discrete_sequence=[color_dict[selected_color]])
            else:
                fig = px.bar(df_combined, x='Periodo', y='Porcentaje', title=f'Indicadores para {selected_color}',
                             color_discrete_sequence=[color_dict[selected_color]], text='Porcentaje')

            fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
            fig.update_layout(yaxis=dict(range=[0, 100]))
        else:
            fig = px.bar(title=f'Sin datos disponibles para {selected_color}')
    else:
        # Si no se ha seleccionado un color, mostrar el gráfico basado en el período y las categorías seleccionadas
        df = convertir_porcentajes(obtener_datos_desde_csv(rangos_periodo.get(selected_time, {'filas': (0, 0), 'columnas': (0, 0)})))
        if not df.empty:
            if not selected_categories:
                selected_categories = df.columns
            try:
                # Filtrar las categorías seleccionadas
                fila_filtrada = df[selected_categories].iloc[0]
                df_temp = pd.DataFrame({
                    'Categoría': fila_filtrada.index,
                    'Porcentaje': fila_filtrada.values
                })
                # Normalizar los nombres de las categorías
                df_temp['Categoría'] = df_temp['Categoría'].str.strip().str.upper()
                # Asignar colores basados en los nombres de las categorías
           # Asignar colores basados en los nombres de las categorías
                df_temp['Color'] = df_temp['Categoría'].map(lambda x: color_dict.get(x.strip().upper(), 'gray'))

                fig = px.bar(df_temp, x='Categoría', y='Porcentaje',
             labels={'Categoría': 'Categoría', 'Porcentaje': 'Porcentaje'},
             title=f'Indicadores De Torres {selected_time}',
             color='Categoría',
             color_discrete_map=color_dict
            )

                if selected_chart == 'bar':
                    fig = px.bar(df_temp, x='Categoría', y='Porcentaje', title=f'Indicadores De Torres {selected_time}',
                                 color='Categoría', color_discrete_map=color_dict)
                elif selected_chart == 'line':
                    fig = px.line(df_temp, x='Categoría', y='Porcentaje', title=f'Indicadores De Torres {selected_time}',
                                  color='Categoría', color_discrete_map=color_dict, markers=True)
                elif selected_chart == 'pie':
                    fig = px.pie(df_temp, values='Porcentaje', names='Categoría', title=f'Indicadores De Torres {selected_time}')
                elif selected_chart == 'scatter':
                    fig = px.scatter(df_temp, x='Categoría', y='Porcentaje', title=f'Indicadores De Torres {selected_time}',
                                     color='Categoría', color_discrete_map=color_dict)
                elif selected_chart == 'area':
                    fig = px.area(df_temp, x='Categoría', y='Porcentaje', title=f'Indicadores De Torres {selected_time}',
                                  color='Categoría', color_discrete_map=color_dict)
                else:
                    fig = px.bar(df_temp, x='Categoría', y='Porcentaje', title=f'Indicadores De Torres {selected_time}',
                                 color='Categoría', color_discrete_map=color_dict)
                fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
                fig.update_layout(yaxis=dict(range=[0, 100]))
            except Exception as e:
                fig = px.bar(title='Error al crear el gráfico')
                print(f"Error al crear el gráfico: {e}")
        else:
            fig = px.bar(title='Sin datos disponibles')
    return fig
