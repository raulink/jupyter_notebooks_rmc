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
        html.Label('Seleccione el tipo de gráfico:'),
        dcc.Dropdown(
            id='tipo-grafico-dropdown-1',
            options=[{'label': tipo, 'value': tipo} for tipo in graph_type_options],
            value='Barra'  # Valor predeterminado
        ),
    ], style={'width': '23%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    html.Br(),

    # Contenedor donde se generarán los dashboards
    html.Div(id='dashboard-container')
])
html.Br(),
# Callback para actualizar ambos gráficos basado en la selección de periodo, línea, categoría y tipo de gráfico
@callback(
    Output('dashboard-container', 'children'),
    [Input('tiempo-dropdown-1', 'value'),
     Input('linea-dropdown-1', 'value'),
     Input('tipo-grafico-dropdown-1', 'value')]
)
def update_dashboards(selected_time, selected_line, selected_graph_type):
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

    # Contenedor para almacenar las gráficas generadas
    dashboard_figures = []

    # Verificar si se seleccionó "MOSTRAR DATOS TODOS LOS MESES"
    if selected_time == 'MOSTRAR DATOS TODOS LOS MESES':
        # Iterar sobre todas las categorías en el mapa de columnas para la línea seleccionada
        for category in category_options:
            df_con_combined = pd.DataFrame()
            df_sin_combined = pd.DataFrame()

            for month in ['MENSUAL 05', 'MENSUAL 06', 'MENSUAL 07', 'MENSUAL 08', 'MENSUAL 09', 'MENSUAL 10']:
                # Verificar si la línea y la categoría están en el mapeo del mes actual
                if month in column_map and selected_line in column_map[month] and category in column_map[month][selected_line]:
                    column = column_map[month][selected_line].get(category, None)
                    
                    # Verificar si la columna existe en el DataFrame
                    if column and column in df.columns:
                        # Filtrar y preparar datos para "CON CABINAS"
                        df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
                        df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
                        df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                        df_con['Mes'] = month
                        df_con['Categoría'] = category  # Agregar la categoría al DataFrame
                        df_con_combined = pd.concat([df_con_combined, df_con], ignore_index=True)

                        # Filtrar y preparar datos para "SIN CABINAS"
                        df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
                        df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
                        df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})
                        df_sin['Mes'] = month
                        df_sin['Categoría'] = category  # Agregar la categoría al DataFrame
                        df_sin_combined = pd.concat([df_sin_combined, df_sin], ignore_index=True)

            # Verificar si los DataFrames están vacíos antes de crear los gráficos
            if not df_con_combined.empty:
                fig_con = generate_graph(df_con_combined, 'Mes', 'Valor', color, selected_graph_type, f'CON CABINAS - {category}', group_bars=True)
                dashboard_figures.append(html.Div(dcc.Graph(figure=fig_con), style={'margin': '20px'}))

            if not df_sin_combined.empty:
                fig_sin = generate_graph(df_sin_combined, 'Mes', 'Valor', color, selected_graph_type, f'SIN CABINAS - {category}', group_bars=True)
                dashboard_figures.append(html.Div(dcc.Graph(figure=fig_sin), style={'margin': '20px'}))

    # Si se selecciona un mes específico en lugar de "MOSTRAR DATOS TODOS LOS MESES"
    else:
        selected_categories = column_map.get(selected_time, {}).get(selected_line, {}).keys()

        for category in selected_categories:
            column = column_map[selected_time][selected_line].get(category, None)

            if column and column in df.columns:
                # Filtrar datos para "CON CABINAS"
                df_con = df[df['Tareas'].str.contains('CON', na=False)][['Unnamed: 1', column]].copy()
                df_con[column] = pd.to_numeric(df_con[column], errors='coerce')
                df_con = df_con.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

                # Filtrar datos para "SIN CABINAS"
                df_sin = df[df['Tareas'].str.contains('SIN', na=False)][['Unnamed: 1', column]].copy()
                df_sin[column] = pd.to_numeric(df_sin[column], errors='coerce')
                df_sin = df_sin.rename(columns={column: 'Valor', 'Unnamed: 1': 'Descripción'})

                # Crear las figuras "CON CABINAS" y "SIN CABINAS" sin el modo agrupado
                fig_con = generate_graph(df_con, 'Descripción', 'Valor', color, selected_graph_type, f'CON CABINAS - {category} - {selected_time}', group_bars=False)
                fig_sin = generate_graph(df_sin, 'Descripción', 'Valor', color, selected_graph_type, f'SIN CABINAS - {category} - {selected_time}', group_bars=False)

                # Agregar ambos gráficos al contenedor de dashboards
                dashboard_figures.extend([
                    html.Div(dcc.Graph(figure=fig_con), style={'margin': '20px'}),
                    html.Div(dcc.Graph(figure=fig_sin), style={'margin': '20px'})
                ])

    return dashboard_figures
def generate_graph(df, x_column, y_column, color, graph_type, title, group_bars=False):
    if graph_type == 'Barra':
        fig = px.bar(df, x=x_column, y=y_column, color='Descripción', title=title, barmode='group' if group_bars else 'relative', text=y_column)
        fig.update_traces(marker=dict(color=color))

    elif graph_type == 'Línea':
        if not df.empty:
            # Si estamos en "MOSTRAR DATOS TODOS LOS MESES", mostramos cada punto como una secuencia continua sin saltos
            if x_column == 'Mes' and len(df[x_column].unique()) > 1:
                # Crear una columna de orden para asegurar la continuidad de la línea
                df['Orden'] = df['Mes'] + ' ' + df['Descripción']
                
                # Convertir 'Orden' a una categoría ordenada para mantener el orden en el gráfico
                df['Orden'] = pd.Categorical(df['Orden'], ordered=True, categories=sorted(df['Orden'].unique()))
                df = df.sort_values(by=['Orden']).reset_index(drop=True)

                # Nos aseguramos de que el valor sea numérico y quitamos NaN
                df[y_column] = pd.to_numeric(df[y_column], errors='coerce')
                df = df.dropna(subset=[y_column])  # Eliminamos valores no numéricos

                # Graficar utilizando 'Orden' como eje x para una línea continua
                fig = px.line(df, x='Orden', y=y_column, title=title, markers=True)
                fig.update_traces(marker=dict(size=6, color=color), line=dict(width=2, color=color))

                # Agregar línea de tendencia para todos los puntos
                try:
                    x_values = np.arange(len(df))
                    z = np.polyfit(x_values, df[y_column], 1)
                    p = np.poly1d(z)
                    fig.add_scatter(
                        x=df['Orden'],
                        y=p(x_values),
                        mode='lines',
                        name='Tendencia',
                        line=dict(color='black', width=2, dash='dash')
                    )
                except np.linalg.LinAlgError:
                    print("Advertencia: No se pudo calcular la línea de tendencia debido a problemas con los datos.")
                
                fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

            else:
                # Gráfico para meses individuales
                df = df.sort_index()
                fig = px.line(df, x=x_column, y=y_column, title=title, markers=True)
                fig.update_traces(marker=dict(size=6), line=dict(width=2, color=color))

                # Línea de tendencia para los meses individuales
                if len(df[x_column].unique()) > 1:
                    try:
                        x_values = np.arange(len(df))
                        z = np.polyfit(x_values, df[y_column], 1)
                        p = np.poly1d(z)
                        fig.add_scatter(
                            x=df[x_column],
                            y=p(x_values),
                            mode='lines',
                            name='Tendencia',
                            line=dict(color='black', width=2, dash='dash')
                        )
                    except np.linalg.LinAlgError:
                        print("Advertencia: No se pudo calcular la línea de tendencia debido a problemas con los datos.")
                fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    elif graph_type == 'Dispersión':
        if not df.empty:
            df = df.sort_index()
            fig = px.scatter(df, x=x_column, y=y_column, title=title)
            fig.update_traces(marker=dict(size=8, color=color))

            if len(df[x_column].unique()) > 1:
                try:
                    x_values = np.arange(len(df))
                    z = np.polyfit(x_values, df[y_column], 1)
                    p = np.poly1d(z)
                    fig.add_scatter(
                        x=df[x_column],
                        y=p(x_values),
                        mode='lines',
                        name='Tendencia',
                        line=dict(color='black', width=2, dash='dash')
                    )
                except np.linalg.LinAlgError:
                    print("Advertencia: No se pudo calcular la línea de tendencia debido a problemas con los datos.")
            fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))

    fig.update_layout(
        title=title,
        xaxis_title='Orden',
        yaxis_title=y_column,
        legend_title_text='Descripción',
        xaxis=dict(showline=True, showgrid=False, zeroline=False, tickangle=45),
        yaxis=dict(showline=True, showgrid=True, zeroline=False)
    )
    return fig



#yopiiiiiiiiiiii funciona sin la linea de tendencia88
#yoppii funciona funcionaaa 1