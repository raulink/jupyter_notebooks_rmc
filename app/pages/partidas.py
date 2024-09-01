import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc

# Leer el archivo de Excel
excel_file = 'Partidas_20240826.120509.xlsx'
df = pd.read_excel(excel_file, sheet_name='Partidas_20240826.120509', skiprows=0, usecols='A:H', nrows=423)

# Convertir todas las columnas a cadenas de texto para asegurar el filtrado correcto
df = df.astype(str)

# Definir el layout de la sección del botón
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Gestión de Partidas Presupuestarias', 
                        className='text-center my-4'), 
                width={'size': 12}),
    ]),
    
    dbc.Row([
        # Fila para el botón de reiniciar filtros
        dbc.Row([
            dbc.Col([
                dbc.Button('Reiniciar Filtros', id='reset-filters-button', color='warning', className='mt-3 mb-4'),
            ], width={'size': 12, 'order': 3}, lg={'size': 10}, md={'size': 10}, sm={'size': 12}, xs={'size': 12}),
        ], justify='center'),
        
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                page_size=20,
                filter_action='native',  # Habilitar el filtrado nativo
                style_table={
                    'overflowX': 'auto',
                    'minWidth': '100%',  # Asegura que la tabla ocupe todo el ancho disponible
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '80px',  
                },
            ),
        ], width={'size': 12, 'order': 1}, lg={'size': 10}, md={'size': 10}, sm={'size': 12}, xs={'size': 12}),
    ], justify='center'),
    
    # Fila para el contador de elementos
    dbc.Row([
        dbc.Col([
            html.P(id='element-counter', className='text-start mt-2'),
        ], width={'size': 12, 'order': 2}, lg={'size': 10}, md={'size': 10}, sm={'size': 12}, xs={'size': 12}),
    ], justify='center'),
    
    # Fila para el botón de reiniciar filtros
], fluid=True)

# Definir el callback para actualizar el contador de elementos
@callback(
    Output('element-counter', 'children'),
    Input('table', 'derived_virtual_data')
)
def update_counter(rows):
    # Si no hay filas, mostrar que no hay elementos
    if rows is None:
        return f'Total: 0 Elemento(s)'
    
    # Contar el número de filas visibles en la tabla
    count = len(rows)
    return f'Total: {count} Elemento(s)'

# Callback para reiniciar los filtros
@callback(
    Output('table', 'filter_query'),
    Input('reset-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    if n_clicks:
        return ''  # Reiniciar los filtros, devolviendo la tabla a su estado original
    return ''