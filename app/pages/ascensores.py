# pages/ascensores.py
import dash
from dash import dcc, html, dash_table, Input, Output
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import date
import os
import dash_bootstrap_components as dbc
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de conexión a MySQL
host = "192.168.100.60"
user = "zona1"
password = "Sistemas0."
database = "opmt2"

# Ruta del archivo Excel
def obtener_ruta_excel():
    return os.path.join(os.path.dirname(__file__), "estacionestado.xlsx")


# Función para obtener datos de MySQL
def obtener_datos_ascensores():
    ruta_excel = obtener_ruta_excel()
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_excel}")

    try:
        logging.debug(f"Conectando a la base de datos: host={host}, user={user}, database={database}")
        conexion = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conexion.cursor()
        query = """
            SELECT a.nestacion, a.linea, a.codigo_asc, a.fecha_inicial, a.fecha_final, a.observaciones
            FROM ascensores a
            INNER JOIN (
                SELECT nestacion, linea, codigo_asc, MAX(fecha_inicial) AS ultima_fecha
                FROM ascensores
                WHERE tipo_mant = 'interrupcion' AND YEAR(fecha_inicial) = 2025
                GROUP BY nestacion, linea, codigo_asc
            ) ult
            ON a.codigo_asc = ult.codigo_asc
            AND a.nestacion = ult.nestacion
            AND a.linea = ult.linea
            AND a.fecha_inicial = ult.ultima_fecha
            ORDER BY a.linea, a.nestacion, a.codigo_asc;
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        df_sql = pd.DataFrame(resultados, columns=["nestacion", "linea", "codigo_asc", "fecha_inicial", "fecha_final", "observaciones"])
        df_sql["Estado"] = df_sql["fecha_final"].apply(lambda x: "Inoperativo" if pd.isna(x) or x == "" else "Operativo")

        # Cargar datos desde Excel, manejando la posible ausencia de la columna 'Estacion'
        try:
            df_excel = pd.read_excel(ruta_excel, usecols=["linea", "nestacion", "codigo_asc", "Estacion"], engine="openpyxl")
            
        except ValueError as e:
            if "Usecols do not match columns" in str(e):
        
                df_excel = pd.DataFrame(columns=["linea", "nestacion", "codigo_asc"])
            else:
                raise

        # Convertir los valores a string y limpiar espacios
        for col in ["linea", "nestacion", "codigo_asc"]:
            if col in df_excel.columns:
                df_excel[col] = df_excel[col].astype(str).str.strip().str.upper()

        df_sql["linea"] = df_sql["linea"].astype(str).str.strip().str.upper()
        df_sql["nestacion"] = df_sql["nestacion"].astype(str).str.strip().str.upper()
        df_sql["codigo_asc"] = df_sql["codigo_asc"].astype(str).str.strip().str.upper()

        # Unir df_excel con df_sql y asegurarnos de incluir 'Estacion'
        if df_excel.empty:
            logging.warning("El DataFrame df_excel está vacío.  Devolviendo df_sql sin unión.")
            df_merged = df_sql
        else:
            df_merged = df_excel.merge(
                df_sql[["nestacion", "linea", "codigo_asc", "Estado", "fecha_inicial", "fecha_final", "observaciones"]],
                on=["nestacion", "linea", "codigo_asc"],
                how="left",
            )
            df_merged["Estado"] = df_merged["Estado"].fillna("Operativo")

        # Renombrar columnas para la tabla
        columnas_renombradas = {
            "linea": "LINEA",
            "nestacion": "ESTACION",
            "codigo_asc": "CÓDIGO ASCENSOR",
            "Estacion": "NOMBRE",  # <- Se corrige el nombre de la columna aquí
            "Estado": "ESTADO",
            "fecha_inicial": "FECHA INICIAL",
            "fecha_final": "FECHA FINAL",
            "observaciones": "Observaciones",
        }
        df_merged.rename(columns=columnas_renombradas, inplace=True)
        return df_merged
    except mysql.connector.Error as err:
        logging.error(f"Error de conexión a la base de datos: {err}")
        return pd.DataFrame()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()



# Función para interrupciones
def obtener_datos_mantenimiento(fecha_inicio, fecha_fin, tipo_mant):
    try:
        conexion = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT linea, nestacion
            FROM ascensores
            WHERE tipo_mant = %s AND fecha_inicial BETWEEN %s AND %s
        """, (tipo_mant, fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        return pd.DataFrame(resultados, columns=["linea", "nestacion"])
    except mysql.connector.Error as err:
        logging.error(f"Error de conexión a MySQL: {err}")
        return pd.DataFrame(columns=["linea", "nestacion"])
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()


def generar_layout_ascensores():
    df_merged = obtener_datos_ascensores()
    if df_merged.empty:
        return html.Div("No hay datos disponibles")
    return dbc.Container(
        [
            dbc.Row(dbc.Col(html.H1("Dashboard de Ascensores", className="text-center text-3xl font-bold mb-6"))),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Estado General de Ascensores", className="text-xl font-semibold mb-2"),
                                dbc.CardBody(dcc.Graph(id="grafico-general"))
                            ]
                        ),
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Tabla de Estados de Ascensores", className="text-xl font-semibold mb-2"),
                                dbc.CardBody(dash_table.DataTable(
                                    id='tabla-ascensores',
                                    columns=[{"name": i, "id": i} for i in df_merged.columns],
                                    data=df_merged.to_dict('records'),
                                    page_size=10,
                                    filter_action='native',
                                    style_table={'overflowX': 'auto'},
                                    style_cell={
                                        'minWidth': '120px', 'maxWidth': '250px', 'whiteSpace': 'normal',
                                        'textAlign': 'left', 'fontFamily': 'Arial Narrow', 'fontSize': '14px',
                                    },
                                    style_header={'backgroundColor': '#333333', 'fontWeight': 'bold',
                                                    'fontFamily': 'Arial Narrow', 'fontSize': '15px', 'color': '#ffffff'},
                                    style_data_conditional=[
                                        {'if': {'filter_query': '{ESTADO} = "Inoperativo"'}, 'backgroundColor': '#EF4444', 'color': 'white'}
                                    ]
                                ))
                            ]
                        ),
                        md=6,
                        className="mb-4",
                    ),
                ],
                className="mb-4"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label("Selecciona una Línea", className="block mb-2"),
                                dcc.Dropdown(
                                    id="filtro-linea",
                                    options=[{"label": linea, "value": linea} for linea in df_merged["LINEA"].unique()],
                                    value=df_merged["LINEA"].unique()[0] if not df_merged.empty else None,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    md=12,
                    className="mb-4"
                ),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                html.Div(id="tabla-filtrada", className="mt-2") # Tabla filtrada a la derecha
                            )
                        ),
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(id="grafico-estados", className="mt-2") # Gráfico de barras filtrado a la izquierda
                            )
                        ),
                        md=6,
                        className="mb-4",
                    ),
                ],
                className="mb-4"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Tipos de Mantenimiento por Líneas", className="text-xl font-semibold text-center mb-4"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(dbc.CardBody(dcc.DatePickerRange(
                                                id="fecha-selector",
                                                start_date=date(2020, 1, 1),
                                                end_date=date(2025, 12, 31),
                                                display_format='DD-MM-YYYY'
                                            ))),
                                            dbc.Col(dbc.CardBody(dcc.Dropdown(
                                                id="tipo-mant-selector",
                                                options=[
                                                    {"label": "Interrupción", "value": "interrupcion"},
                                                    {"label": "Correctivo", "value": "correctivo"},
                                                    {"label": "Preventivo", "value": "preventivo"}
                                                ],
                                                value="interrupcion",
                                                clearable=False,
                                                className="w-100"
                                            )))
                                        ],
                                        className="mb-3"
                                    ),
                                    dcc.Graph(id="grafico-interrupciones")
                                ]
                            )
                        ]
                    ),
                    md=12
                )
            )
        ],
        fluid=True
    )


# Mantén tus callbacks exactamente igual como estaban antes, no necesitas modificaciones ahí.
def crear_callbacks_ascensores(app):
    @app.callback(
        [Output("grafico-estados", "figure"),
         Output("grafico-general", "figure"),
         Output("tabla-filtrada", "children")],
        [Input("filtro-linea", "value")]
    )
    
    def actualizar_graficos_y_tabla(linea):
            df = obtener_datos_ascensores()
            df_filtrado = df[df["LINEA"] == linea] if linea else df
            conteo = df_filtrado.groupby(["ESTADO", "ESTACION"]).size().reset_index(name="Cantidad")
            fig1 = px.bar(conteo, x="ESTACION", y="Cantidad", color="ESTADO",
                            color_discrete_map={'Operativo': 'green', 'Inoperativo': 'red'}, text="Cantidad")
            fig1.update_traces(textposition='inside', textfont_size=14)

            # Generar el gráfico de pastel con el DataFrame original (sin filtrar)
            total = df["ESTADO"].value_counts()
            fig2 = px.pie(values=total.values, names=total.index,
                            color=total.index, color_discrete_map={'Operativo': 'green', 'Inoperativo': 'red'})

            tabla = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df_filtrado.columns],
                data=df_filtrado.to_dict("records"),
                page_size=10,
                style_table={'overflowX': 'auto'},
                filter_action='native',
                style_cell={
                    'minWidth': '120px', 'maxWidth': '250px', 'whiteSpace': 'normal',
                    'textAlign': 'left', 'fontFamily': 'Arial Narrow', 'fontSize': '14px',
                },
                style_header={'backgroundColor': '#333333', 'fontWeight': 'bold',
                                'fontFamily': 'Arial Narrow', 'fontSize': '15px', 'color': '#ffffff'},
                style_data_conditional=[
                    {'if': {'filter_query': '{ESTADO} = "Inoperativo"'}, 'backgroundColor': '#EF4444', 'color': 'white'}
                ]
            )
            return fig1, fig2, html.Div(tabla)

    @app.callback(
        Output("grafico-interrupciones", "figure"),
        [Input("fecha-selector", "start_date"),
         Input("fecha-selector", "end_date"),
         Input("tipo-mant-selector", "value")]
    )
    def actualizar_grafico_interrupciones(fecha_inicio, fecha_fin, tipo_mant):
        df = obtener_datos_mantenimiento(fecha_inicio, fecha_fin, tipo_mant)
        if df.empty:
            return px.bar(title="No hay datos disponibles")
        df_grouped = df.groupby(["linea", "nestacion"]).size().reset_index(name="count")
        fig = px.bar(df_grouped, x="linea", y="count", color="nestacion",
                      title=f"Tipo de Mantenimiento - {tipo_mant.capitalize()} ({fecha_inicio} - {fecha_fin})",
                      text="count")
        fig.update_traces(textposition='outside')
        fig.update_layout(title_x=0.5)
        return fig