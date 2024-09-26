from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
from pages import procesos
from pages import dashboard, linearoja, partidas, grafico_ingreso, grafico_salida, operaciones, indicadoresDeTorres

# Crear instancia de la aplicación Dash y agregar hoja de estilo CSS
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/morph/bootstrap.min.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server  # Esta es la instancia Flask subyacente

# Crear la barra lateral deslizable (Offcanvas)
sidebar = dbc.Offcanvas(
    [
        html.A(
            html.Img(src="/assets/logo1.png", height="100px"),
            href="/",
            style={"textDecoration": "none"},
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard OTs", href="/dashboard", active="exact"),
                dbc.NavLink("Indicadores", href="/linearoja", active="exact"),
                dbc.NavLink("Partidas presupuestarias", href="/partidas", active="exact"),
                dbc.NavLink("Gráfico de Ingresos", href="/grafico_ingreso", active="exact"),
                dbc.NavLink("Gráfico de Salidas", href="/grafico_salida", active="exact"),
                dbc.NavLink("Dashboard Operaciones", href="/operaciones", active="exact"),
                
                # Mover el DropdownMenu dentro del dbc.Nav
                dbc.DropdownMenu(
                    label="INDICADORES DE CONFIABILIDAD",
                    children=[
                        dbc.DropdownMenuItem("Indicadores de torres", href="/indicadoresDeTorres"),
                    ],
                    nav=True,
                    in_navbar=False,  # Esto asegura que el menú esté en el sidebar y no en la navbar
                    toggle_style={"width": "100%"},  # Ajustar el botón a todo el ancho
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="offcanvas-sidebar",
    is_open=False,
    style={'background-color': '#f8f9fa', 'padding': '20px'}
)


# Crear la barra superior con un botón tipo "sandwich"
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    dbc.Button(
                        html.Img(src="/assets/logo.png", height="40px"),
                        id="open-offcanvas",
                        style={"background": "none", "border": "none"},
                    ),
                    width="auto",
                ),
                justify="start",
                className="g-0",
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    style={"padding-left": "0px"}  # Asegura que no haya padding a la izquierda
)



# Imagen para mostrar en la pantalla principal
main_image = html.Img(src="/assets/miteleferico.png", style={"width": "100%", "height": "auto"})

# Definir el diseño principal de la aplicación
app.layout = dbc.Container(
    [
        navbar,
        sidebar,  # Agregar la barra lateral aquí
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Location(id='url', refresh=False),
                        html.Div(id='page-content', style={'padding': '20px'})
                    ],
                    width=12
                ),
            ]
        ),
    ],
    fluid=True,
    style={"padding": "0"}
)

# Callback para controlar la apertura y cierre del Offcanvas
@app.callback(
    Output("offcanvas-sidebar", "is_open"),
    [Input("open-offcanvas", "n_clicks")],
    [State("offcanvas-sidebar", "is_open")],
)
def toggle_offcanvas(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Definir la lógica de enrutamiento para mostrar el contenido de la página
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def display_page(pathname):
    if pathname == '/' or pathname == '':
        return main_image  # Mostrar la imagen principal cuando no se selecciona ninguna opción
    elif pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/linearoja':
        return linearoja.layout
    elif pathname == '/partidas': 
        return partidas.layout
    elif pathname == '/grafico_ingreso':
        return grafico_ingreso.layout
    elif pathname == '/grafico_salida':
        return grafico_salida.layout
    elif pathname == '/operaciones':
        return operaciones.layout
    elif pathname == '/indicadoresDeTorres': 
         return indicadoresDeTorres.layout
    elif pathname == '/procesos': 
         return procesos.layout
     
    else:
        return dbc.Alert("404 - Página no encontrada", color="danger")

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
