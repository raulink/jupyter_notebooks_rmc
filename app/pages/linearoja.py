import io
import plotly.io as pio
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_table
import plotly.graph_objects as go
import pandas as pd

# Constantes para configuraciones de estilos
STYLE_CENTER = {'textAlign': 'center'}
STYLE_INLINE_BLOCK = {'display': 'inline-block', 'verticalAlign': 'top'}
STYLE_TABLE = {'overflowX': 'scroll'}
STYLE_CELL = {'textAlign': 'center'}
STYLE_HEADER = {'fontWeight': 'bold'}

# Ruta al archivo de Excel
EXCEL_FILE = 'Ingresos 2017-20241.xlsx'

# Diccionario de secciones
SECCIONES = {
    'DISPONIBILIDAD': (0, 8),
    'CONFIABILIDAD': (9, 17),
    'TIEMPO MEDIO ENTRE FALLAS (MTBF)': (18, 26),
    'TIEMPO MEDIO DE RESPUESTA (MTTA)': (27, 35),
    'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)': (36, 44)
}

def obtener_datos_seccion(línea, seccion):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=línea, skiprows=0, usecols='A:H', nrows=44)
    except FileNotFoundError:
        raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
    except Exception as e:
        raise Exception(f"Error al leer el archivo de Excel: {e}")
    
    start_row, end_row = SECCIONES[seccion]
    df_seccion = df.iloc[start_row:end_row].copy()

    # Calcular el promedio o máximo según la sección
    if seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
        df_seccion.iloc[:, 1:] = df_seccion.iloc[:, 1:].stack().apply(
            lambda x: x.hour * 3600 + x.minute * 60 + x.second).unstack()
        
        if seccion == 'TIEMPO MEDIO DE RESPUESTA (MTTA)':
            df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].mean(axis=1)
        else:
            df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].max(axis=1)
        
        df_seccion['PROMEDIO'] = pd.to_datetime(df_seccion['PROMEDIO'], unit='s').dt.time
    else:
        df_seccion['PROMEDIO'] = df_seccion.iloc[:, 1:].mean(axis=1)

    return df_seccion

def obtener_datos_resumen_total():
    try:
        df_resumen_total = pd.read_excel(EXCEL_FILE, sheet_name='resumentotal', skiprows=8, usecols='B:F', nrows=11)
    except FileNotFoundError:
        raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
    except Exception as e:
        raise Exception(f"Error al leer el archivo de Excel: {e}")
    
    df_resumen_total.columns = ['DISPONIBILIDAD', 'CONFIABILIDAD', 'MTBF', 'MTTA', 'MTTR']
    df_resumen_total.insert(0, 'Línea', ['Línea Roja', 'Línea Verde', 'Línea Amarilla', 'Línea Azul', 'Línea Naranja', 
                                         'Línea Blanca', 'Línea Celeste', 'Línea Morada', 'Línea Plateada', 'Línea Café'])

    return df_resumen_total

def obtener_datos_tabla(línea):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=línea, usecols='J:N', nrows=2, header=None)
    except FileNotFoundError:
        raise Exception(f"El archivo {EXCEL_FILE} no se encontró.")
    except Exception as e:
        raise Exception(f"Error al leer el archivo de Excel: {e}")
    
    # Los encabezados están en la primera fila (fila 0) y los datos en la segunda fila (fila 1)
    headers = df.iloc[0].tolist()
    values = df.iloc[1].tolist()
    
    return headers, values

# Layout de la aplicación
layout = html.Div([
    html.H1('Indicadores por Línea', style=STYLE_CENTER),

    html.Div([
        html.Label('Selecciona Línea:'),
        dcc.Dropdown(
            id='linea-dropdown',
            options=[
                {'label': 'Línea Roja', 'value': 'linearoja'},
                {'label': 'Línea Verde', 'value': 'lineaverde'},
                {'label': 'Línea Amarilla', 'value': 'lineaamarilla'},
                {'label': 'Línea Azul', 'value': 'lineaazul'},
                {'label': 'Línea Naranja', 'value': 'lineanaranja'},
                {'label': 'Línea Blanca', 'value': 'lineablanca'},
                {'label': 'Línea Celeste', 'value': 'lineaceleste'},
                {'label': 'Línea Morada', 'value': 'lineamorada'},
                {'label': 'Línea Plateada', 'value': 'lineaplateada'},
                {'label': 'Línea Café', 'value': 'lineacafe'},
                {'label': 'Resumen Total', 'value': 'resumentotal'}  # Nueva opción
            ],
            value='linearoja',
            clearable=False
        ),
    ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

    html.Div([
        html.Label('Selecciona Sección:'),
        dcc.Dropdown(
            id='seccion-dropdown',
            options=[{'label': key, 'value': key} for key in SECCIONES.keys()],
            value='DISPONIBILIDAD',
            clearable=False
        ),
    ], style={**STYLE_CENTER, 'paddingBottom': '20px', 'width': '45%', 'margin': 'auto'}),

    html.Div([
        dcc.Graph(id='histograma-linea', style={**STYLE_INLINE_BLOCK, 'width': '85%', 'textAlign': 'center'}),
        
        html.Div([
            html.Label('Selecciona Sistemas:'),
            dcc.Checklist(
                id='sistemas-checklist',
                value=[],
                inline=False
            ),
            html.Br(),
            html.Label('Selecciona el tipo de gráfico:'),
            dcc.Dropdown(
                id='tipo-grafico',
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
            html.Button('Exportar a PDF', id='export-pdf-button', n_clicks=0)
        ], style={**STYLE_INLINE_BLOCK, 'width': '15%', 'paddingLeft': '10px', 'textAlign': 'left'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

    html.Div([
        html.H2('Resumen de Indicadores por Linea', style=STYLE_CENTER),
        dash_table.DataTable(
            id='tabla-linea',
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
            id='tabla-resumen',
            columns=[],
            data=[],
            style_table=STYLE_TABLE,
            style_cell=STYLE_CELL,
            style_header=STYLE_HEADER,
        )
    ], style={'marginTop': '20px', 'textAlign': 'center'}),
    dcc.Download(id='download-pdf')
], style=STYLE_CENTER)


@callback(
    [Output('sistemas-checklist', 'options'),
     Output('sistemas-checklist', 'value'),
     Output('tabla-linea', 'columns'),
     Output('tabla-linea', 'data')],
    [Input('linea-dropdown', 'value'),
     Input('seccion-dropdown', 'value')]
)
def actualizar_seccion(línea, seccion):
    if línea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        Sistemas = df_resumen_total['Línea'].tolist()
        columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
        data = df_resumen_total.to_dict('records')
        return [{'label': line, 'value': line} for line in Sistemas], Sistemas, columns, data
    else:
        df_seccion = obtener_datos_seccion(línea, seccion)
        Sistemas = df_seccion.iloc[:, 0].tolist()
        columns = [{'name': col, 'id': col} for col in df_seccion.columns]
        data = df_seccion.to_dict('records')
        return [{'label': line, 'value': line} for line in Sistemas], Sistemas, columns, data

@callback(
    Output('histograma-linea', 'figure'),
    [Input('sistemas-checklist', 'value'),
     Input('tipo-grafico', 'value'),
     Input('linea-dropdown', 'value'),
     Input('seccion-dropdown', 'value')]
)
def update_histogram(selected_Sistemas, tipo_grafico, línea, seccion):
    fig = go.Figure()

    # Determinar el modo de apilado o agrupado para gráficos de barras o columnas
    if tipo_grafico in ['bar_stacked', 'col_stacked']:
        barmode = 'stack'
    elif tipo_grafico in ['bar_grouped', 'col_grouped']:
        barmode = 'group'
    else:
        barmode = None  # No apilamiento para gráficos de líneas
    
    if línea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        filtered_df = df_resumen_total[df_resumen_total['Línea'].isin(selected_Sistemas)]
        
        if seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
            for col in ['MTTA', 'MTTR']:
                if col in filtered_df.columns:
                    if tipo_grafico == 'line':
                        fig.add_trace(go.Scatter(
                            x=filtered_df['Línea'],
                            y=filtered_df[col],
                            mode='lines+markers',
                            name=col
                        ))
                    else:
                        fig.add_trace(go.Bar(
                            x=filtered_df['Línea'] if tipo_grafico.startswith('bar') else filtered_df[col],
                            y=filtered_df[col] if tipo_grafico.startswith('bar') else filtered_df['Línea'],
                            name=col,
                            orientation='h' if tipo_grafico.startswith('col') else 'v'
                        ))

            # Ajustar el eje Y para MTTA y MTTR en segundos
            min_val = filtered_df[['MTTA', 'MTTR']].min().min()
            max_val = filtered_df[['MTTA', 'MTTR']].max().max()

            tickvals = list(range(int(min_val), int(max_val) + 1, max(1, int((max_val - min_val) / 8))))
            ticktext = [pd.to_datetime(val, unit='s').strftime('%H:%M:%S') for val in tickvals]

            fig.update_yaxes(
                range=[min_val, max_val],
                tickvals=tickvals,
                ticktext=ticktext,
                autorange="reversed"  # Esto asegura que el eje Y esté en orden ascendente
            )
        else:
            for col in df_resumen_total.columns[1:]:
                if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                    fig.add_trace(go.Bar(x=filtered_df['Línea'], y=filtered_df[col], name=col))
                elif tipo_grafico in ['col_stacked', 'col_grouped']:
                    fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df['Línea'], name=col, orientation='h'))
                elif tipo_grafico == 'line':
                    fig.add_trace(go.Scatter(x=filtered_df['Línea'], y=filtered_df[col], mode='lines+markers', name=col))

    else:
        df_seccion = obtener_datos_seccion(línea, seccion)
        filtered_df = df_seccion[df_seccion.iloc[:, 0].isin(selected_Sistemas)]

        for col in df_seccion.columns[1:-1]:
            if tipo_grafico in ['bar_stacked', 'bar_grouped']:
                fig.add_trace(go.Bar(x=filtered_df.iloc[:, 0], y=filtered_df[col], name=col))
            elif tipo_grafico in ['col_stacked', 'col_grouped']:
                fig.add_trace(go.Bar(x=filtered_df[col], y=filtered_df.iloc[:, 0], name=col, orientation='h'))
            elif tipo_grafico == 'line':
                fig.add_trace(go.Scatter(x=filtered_df.iloc[:, 0], y=filtered_df[col], mode='lines+markers', name=col))
        
        # Trazado para la columna de "PROMEDIO"
        fig.add_trace(go.Scatter(
            x=filtered_df.iloc[:, 0],
            y=filtered_df['PROMEDIO'],
            mode='lines+markers' if tipo_grafico == 'line' else 'markers',
            name='PROMEDIO',
            line=dict(color='orange', width=4, dash='dash') if tipo_grafico == 'line' else None,
            marker_color='orange' if tipo_grafico != 'line' else None
        ))

        # Configuración del eje Y basada en la sección seleccionada
        if seccion == 'DISPONIBILIDAD':
            fig.update_yaxes(
            range=[0.9, 1.0],
            tickformat=".0%",
            tickvals=[0.90 + i * 0.02 for i in range(6)],  # Incrementos de 2.0%
            ticktext=[f"{0.90 + i * 0.02:.1%}" for i in range(6)]
            )
        elif seccion == 'CONFIABILIDAD':
            
            min_val = filtered_df.iloc[:, 1:-1].min().min()
            max_val = 1.0  # 100.0% en formato decimal

            if min_val < 0:
                min_val = min_val
        
            fig.update_yaxes(
                range=[min_val, max_val],
                tickformat=".0%",
                tickvals=[i * 0.2 for i in range(int(max_val * 5 + 1))],  # Incrementos de 20.0%
                ticktext=[f"{i * 20:.0f}%" for i in range(int(max_val * 5 + 1))]
            )
        elif seccion in ['TIEMPO MEDIO ENTRE FALLAS (MTBF)']:
            y_max = filtered_df.iloc[:, 1:-1].values.max()
            y_min = filtered_df.iloc[:, 1:-1].values.min()
            fig.update_yaxes(range=[y_min, y_max])
        
        elif seccion in ['TIEMPO MEDIO DE RESPUESTA (MTTA)', 'TIEMPO MEDIO ENTRE REPARACIONES (MTTR)']:
            y_max = filtered_df.iloc[:, 1:-1].max().max()
            y_min = filtered_df.iloc[:, 1:-1].min().min()
        
            # Generar los valores de tickvals y ticktext como listas
            tickvals = list(range(int(y_min), int(y_max) + 1, max(1, int((y_max - y_min) / 8))))
            ticktext = [pd.to_datetime(val, unit='s').strftime('%H:%M:%S') for val in tickvals]
        
            fig.update_yaxes(
                range=[y_min, y_max],
                tickvals=tickvals,
                ticktext=ticktext
            )

    fig.update_layout(barmode=barmode, yaxis_title='Valores', xaxis_title='Sistemas')
    return fig


@callback(
    Output('download-pdf', 'data'),
    [Input('export-pdf-button', 'n_clicks')],
    [State('histograma-linea', 'figure')]
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


@callback(
    [Output('tabla-resumen', 'columns'),
     Output('tabla-resumen', 'data')],
    [Input('linea-dropdown', 'value')]
)
def update_table(línea):
    if línea == 'resumentotal':
        df_resumen_total = obtener_datos_resumen_total()
        columns = [{'name': col, 'id': col} for col in df_resumen_total.columns]
        data = df_resumen_total.to_dict('records')
    else:
        headers, values = obtener_datos_tabla(línea)
        columns = [{'name': header, 'id': header} for header in headers]
        data = [dict(zip(headers, values))]
    
    return columns, data