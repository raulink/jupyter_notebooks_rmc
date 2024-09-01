import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback

# Ruta al archivo de Excel en la misma carpeta del proyecto
excel_file = 'Ingresos 2017-20241.xlsx'

# Leer datos de la hoja "dashboard" de Excel
df = pd.read_excel(excel_file, sheet_name='dashboard', skiprows=0, usecols='A:AI', nrows=2480)

# Convertir la columna 'created_at' a datetime y hacerla tz-naive
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.tz_localize(None)

# Definir nombres de líneas
line_names = df['linea'].unique()

# Definir los colores personalizados para las categorías
category_colors = {
    'Correctivo': '#1f77b4',  # Azul
    'Mejora': '#ff7f0e',      # Naranja
    'Preventivo': '#2ca02c',  # Verde
    'Soporte': '#d62728'      # Rojo
}

# Definir el layout de la aplicación
layout = html.Div([
    html.H1('Dashboard de OTs'),
    html.Div([
        # Dropdown para seleccionar tipo de gráfico
        html.Label('Selecciona el tipo de gráfico:'),
        dcc.Dropdown(
            id='chart-type-dropdown',
            options=[
                {'label': 'Barras Apiladas', 'value': 'stacked_bar'},
                {'label': 'Columnas Apiladas', 'value': 'stacked_column'},
                {'label': 'Barras Agrupadas', 'value': 'grouped_bar'},
                {'label': 'Columnas Agrupadas', 'value': 'grouped_column'},
            ],
            value='stacked_bar',  # Valor por defecto
            clearable=False,
            style={'width': '50%'}
        ),
        # Gráfico
        dcc.Graph(id='histograma-dashboard'),
    ], style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),
    # Checklist para seleccionar líneas y selector de rango de fechas
    html.Div([
        html.Label('Selecciona Líneas:'),
        dcc.Checklist(
            id='linea-checklist',
            options=[{'label': name, 'value': name} for name in line_names],
            value=list(line_names),  # Inicialmente todas las líneas están seleccionadas
            labelStyle={'display': 'block'},
        ),
        html.Br(),
        html.Label('Selecciona Rango de Fechas:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['created_at'].min().date(),
            end_date=df['created_at'].max().date(),
            display_format='DD/MM/YYYY'
        )
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px', 'textAlign': 'left'})
], style={'textAlign': 'center'})

@callback(
    Output('histograma-dashboard', 'figure'),
    [Input('linea-checklist', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('chart-type-dropdown', 'value')]
)
def update_histogram(selected_lines, start_date, end_date, chart_type):
    # Convertir las fechas seleccionadas a datetime y asegurarse de que sean tz-naive
    try:
        start_date = pd.to_datetime(start_date).tz_localize(None)
        end_date = pd.to_datetime(end_date).tz_localize(None)
    except Exception as e:
        print(f"Error en la conversión de fechas: {e}")
        return {}

    # Filtrar el DataFrame según las líneas seleccionadas y el rango de fechas
    filtered_df = df[(df['created_at'] >= start_date) & 
                     (df['created_at'] <= end_date) & 
                     (df['linea'].isin(selected_lines))]
    
    # Verificar si el DataFrame filtrado está vacío
    if filtered_df.empty:
        return px.bar(title='No hay datos para mostrar')

    # Agrupar por 'linea' y 'Categoria', y contar las ocurrencias
    categoria_count = filtered_df.groupby(['linea', 'Categoria']).size().reset_index(name='counts')

    # Seleccionar tipo de gráfico
    if chart_type == 'stacked_bar':
        orientation = 'h'
        barmode = 'stack'
    elif chart_type == 'stacked_column':
        orientation = 'v'
        barmode = 'stack'
    elif chart_type == 'grouped_bar':
        orientation = 'h'
        barmode = 'group'
    elif chart_type == 'grouped_column':
        orientation = 'v'
        barmode = 'group'

    # Crear el gráfico
    fig = px.bar(
        categoria_count,
        x='counts' if orientation == 'h' else 'linea',
        y='linea' if orientation == 'h' else 'counts',
        color='Categoria',
        color_discrete_map=category_colors,  # Aplicar los colores personalizados
        labels={'counts': 'Recuento de Categoría', 'linea': 'Línea'},
        title='Recuento de Categoría por Línea y Categoría',
        orientation=orientation,  # Configuración de orientación
    )
    fig.update_layout(
        barmode=barmode, 
        height=510, 
        legend_title_text='Categoría',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig
