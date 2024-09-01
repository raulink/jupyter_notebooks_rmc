# pip install mysql-connector-python pandas

import pymysql
import pandas as pd

# Configura tu conexión a la base de datos
config = {
    'user': 'mantto',
    'password': 'Sistemas0,',
    'host': '192.168.100.50',
    'database': 'opmt2'
}

# Establece la conexión
conn = pymysql.connect(**config)


# Escribe tu consulta SQL
query = "SELECT * FROM anomalias limit 10"


# Ejecuta la consulta y almacena los resultados en un DataFrame
df = pd.read_sql(query, conn)

# Cierra la conexión
conn.close()

# Muestra el DataFrame

df