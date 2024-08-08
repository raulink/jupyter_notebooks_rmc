# %%
import pandas as pd
import requests


class GoogleSheetToCSV:
    def __init__(self, sheet_url):
        self.sheet_url = sheet_url
        self.spreadsheet_id = self.extract_spreadsheet_id(sheet_url)
        self.sheet_id = self.extract_sheet_id(sheet_url)
        self.csv_export_url = self.construct_csv_export_url()

        # Diccionarios originales
        self.valores = {
            "D": 1,
            "S": 1,
            "M": 5,
            "MC": 1,
            "2M": 2,
            "T": 3,
            "4M": 4,
            "SE": 6,
            "8M": 8,
            "A": 1,
            "1.5A": 18,
            "2A": 2,
            "3A": 3,
            "4A": 4,
            "5A": 5,
            "6A": 6,
            "8A": 8,
            "10A": 10,
            "1000": 1000,
            "6000": 6000,
            "22500": 22500,
            "40000": 40000,
            "55000": 55000
        }

        self.regimen = {
            "D": 'dia',
            "S": 'semana',
            "M": 'semana',
            "MC": 'mes',
            "2M": 'mes',
            "T":  'mes',
            "4M": 'mes',
            "SE": 'mes',
            "8M": 'mes',
            "A": 'Año',
            "1.5A": 'mes',
            "2A": 'Año',
            "3A": 'Año',
            "4A": 'Año',
            "5A": 'Año',
            "6A": 'Año',
            "8A": 'Año',
            "10A": 'Año',
            "1000": 'horas',
            "6000": 'horas',
            "22500": 'horas',
            "40000": 'horas',
            "55000": 'horas'
        }

    def extract_spreadsheet_id(self, url):
        # Extrae el ID de la hoja de cálculo de la URL
        return url.split('/d/')[1].split('/')[0]

    def extract_sheet_id(self, url):
        # Extrae el ID de la hoja específica de la URL
        return url.split('gid=')[1]

    def construct_csv_export_url(self):
        # Construye la URL de exportación a CSV
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&id={self.spreadsheet_id}&gid={self.sheet_id}"

    def download_csv(self, output_filename='temp_sheet.csv'):
        # Descarga el archivo CSV y lo guarda temporalmente
        response = requests.get(self.csv_export_url)
        response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        return output_filename

    def set_dataframes(self, df1, df2):
        """
        Inicializa la clase con dos dataframes.

        Args:
            df1 (pd.DataFrame): El primer dataframe.
            df2 (pd.DataFrame): El segundo dataframe.
        """
        self.df1 = df1
        self.df2 = df2

    def buscarv(self, col_a='A', col_b='C', col_res=None):
        """
        Realiza una combinación de los dataframes basándose en las columnas especificadas.

        Args:
            col_a (str): Nombre de la columna en df1 para la combinación.
            col_b (str): Nombre de la columna en df2 para la combinación.
            col_res (str): Nombre de la columna de resultados a retornar. Si es None, retorna todas las columnas combinadas.

        Returns:
            pd.DataFrame: Dataframe con las filas combinadas y las columnas especificadas.
        """
        # Asegurar que las columnas para combinar sean del mismo tipo
        self.df1[col_a] = self.df1[col_a].astype(str)
        self.df2[col_b] = self.df2[col_b].astype(str)

        result = pd.merge(self.df1, self.df2, how='inner',
                          left_on=col_a, right_on=col_b)
        if col_res is None:
            return result
        else:
            return result[[col_a, col_res]]

    def get_unique(self, df: pd.DataFrame, column: str):
        """
        Obtiene un DataFrame con valores únicos de la columna 'Column', con índices ajustados.

        Returns:
        pd.DataFrame: Un DataFrame con valores únicos de la columna 'Column' y un índice ajustado.
        """
        df[column] = df[column].str.strip()
        df = df[df[column].notnull()]
        df_unique = pd.DataFrame(df[column].unique(), columns=['value'])
        df_unique.index = df_unique.index + 1
        return df_unique

    def asignar_frecuencias(self, row, parametros):
        # Verificar que los diccionarios tengan el mismo tamaño
        if len(parametros['valores']) != len(parametros['regimen']):
            raise ValueError(f"Los diccionarios no tienen el mismo tamaño. {len(parametros['cabecera'])} != {len(parametros['regimen'])}")

        # Asignar valores a la columna "regimen frecuencia"
        for key in parametros['cabecera']:
            if row[key] == True:
                return parametros['regimen']

        return None

    def get_regime(
        self,
        df: pd.DataFrame,
        parametros: dict        
    ):
        """
        Obtiene un DataFrame, realiza la clasificación por frecuencias y por unidades.

        Returns:
        pd.DataFrame: Un DataFrame con 2 Columnas value y unidad de acuerdo a las frecuencias de sus mantenimientos.
        """
        # Aplicar la función a cada columna en la lista
        # columnas = ['D', 'S', 'M', 'MC', '2M', 'T', '4M','SE', '8M', 'A', '1.5A', '2A', '3A', '4A', '5A', '6A', '8A', '10A','1000', '6000', '22500', '40000', '55000']
        # Conversion en valores booleanos
        df[list(self.valores.keys())] = df[self.valores.keys()].applymap(lambda x: True if x == 'TRUE' else False)

        df['unidad'] = df.apply(lambda x: self.asignar_frecuencias(x, parametros), axis=1)
        df['valor'] = df.apply(
            lambda x: self.asignar_frecuencias(x, parametros), axis=1)
        df1 = df[['id', 'Cod', 'Plan', 'Accion', 'Actividad', 'Tipo',
                  'Parada', 'Relevancia', 'Especialidad', 'D', 'valor', 'unidad']]
        return df1

    def get_dataframes(self):
        # obtener dataframes de archivo csv
        df = pd.DataFrame(self.read_csv())
        self.df_plans = self.get_unique(df, 'Plan')
        self.df_actions = self.get_unique(df, 'Accion')
        self.df_specialities = self.get_unique(df, 'Especialidad')

        # df_regime = self.get_regime(df,"",calendar="FECHAS",)

    def print_datafarame(self):
        return self.df_plans

    def read_csv(self, filename="temp_sheet.csv"):
        # Lee el archivo CSV usando pandas
        self.df = pd.read_csv(filename)
        self.df.columns = self.df.loc[2, :].to_list()  # la fila 2 como fila
        self.df = self.df.loc[4:, :]   # Obtener desde la fila 4 en adelante
        return self.df

    def get_data_frame(self):
        # Descargar y leer el archivo CSV en un DataFrame
        csv_filename = self.download_csv()
        return self.read_csv(csv_filename)

# %%
import pandas as pd
import os

archivo = "temp_sheet.csv"

# Cargado de plan de actividades
sheet_url = "https://docs.google.com/spreadsheets/d/1OkECu7qNfGZxX_rc2RDbaz0A-oE_gUwJ0P2tjU_x-q0/edit?gid=1199302294#gid=1199302294"
gs = GoogleSheetToCSV(sheet_url)
# Descargar el archivo csv
#gs.download_csv()       # Descarga del csv en el disco
df_raw = gs.read_csv()   # Carga del csv descargado en un dataframe

# %%
# Copiar dataframe
df = df_raw.copy(deep=True)

# %%
## convertir a booleano
df[list(gs.valores.keys())] = df[gs.valores.keys()].applymap(lambda x: True if x == 'TRUE' else False)
# Obtener la unidades
parametros = gs.regimen
df['unidad'] = df.apply(lambda row: next((parametros[key] for key in parametros.keys() if key in row and row[key] == True), None), axis=1)
# Obtener los valores
parametros = gs.valores
df['valor'] = df.apply(lambda row: next((parametros[key] for key in parametros.keys() if key in row and row[key] == True), None), axis=1)
# Filtrar las columnas necesarias solamente

# Quitar planes
df = df[df['Tipo']!= 'Plan']

# Mantener solo las columnas necesarias
columns = ['Plan','Accion','Trabajo','Actividad','Tipo','Parada','Relevancia','Especialidad','valor','unidad']
df = df[columns]

# %%
# Crear la nueva columna fk_activity que tendra relaciones con las actividades padre
df['fk_activity']= None
df['fkc_regime']= None

# renombrar los nombres de las columnas
nuevos_nombres = {
    'Plan': 'fk_plan',
    'Accion': 'fk_action',
    'Actividad': 'name',
    'Tipo': 'fkc_activity_type',
    'Relevancia': 'fkc_priority',
    'Especialidad': 'fk_specialty',
    'valor': 'time_interval_value',
    'unidad': 'fk_periodicity_unit',
    'Parada': 'stoppage',
}
df.rename(columns=nuevos_nombres, inplace=True)


# %%
# Mantener las columnas del excel en el orden indicado
columnas_excel = ['fk_activity','fk_plan','fk_action','name','fkc_activity_type','fkc_priority','fk_specialty','fkc_regime','stoppage','time_interval_value','fk_periodicity_unit'] 

df = df[columnas_excel]

# %%
df_plan = gs.get_unique(df,"fk_plan")
df_action = gs.get_unique(df,"fk_action")
df_speciality = gs.get_unique(df,"fk_specialty")


# %%
# Filter the data
#df = df_raw.copy(deep=True)
filtered_data = df[(df['fkc_activity_type'] == 'Actividad') | (df['fkc_activity_type'] == 'Tarea')]

# Add fk_activity column
filtered_data['fk_activity'] = None

# Set fk_activity for Tareas based on their parent Actividad
parent_index = None
for i, row in filtered_data.iterrows():
    if row['fkc_activity_type'] == 'Actividad':
        parent_index = i
    elif row['fkc_activity_type'] == 'Tarea':
        filtered_data.at[i, 'fk_activity'] = parent_index
filtered_data


# %%
filtered_data

# %%
# Para barrido por filas
conteo_actividad = 1

df
for i,row in df.iterrows():
    
    
    for cell in row:
        print( cell)
    break

# %%


# %%
# Muestreo aleatorio de 5 muestras
df.sample(5)


