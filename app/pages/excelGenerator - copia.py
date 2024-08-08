import pandas as pd
import requests


class GoogleSheetProcessor:
    def __init__(self, sheet_url,file_path):
        self.sheet_url = sheet_url
        self.spreadsheet_id = self.extract_spreadsheet_id(sheet_url)
        self.sheet_id = self.extract_sheet_id(sheet_url)
        self.csv_export_url = self.construct_csv_export_url()
        self.file_path = file_path
        self.df = None
        self.df_plan = None
        self.df_action = None
        self.df_speciality = None
        self.filtered_data = None

        

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

    def read_csv(self, filename="temp_sheet.csv"):
        # Lee el archivo CSV usando pandas
        self.df = pd.read_csv(filename)
        self.df.columns = self.df.loc[2, :].to_list()  # la fila 2 como fila
        self.df = self.df.loc[4:, :]   # Obtener desde la fila 4 en adelante
        return self.df

    def process_data(self):
        # Descargar y leer el archivo CSV en un DataFrame
        csv_filename = self.download_csv()
        df_raw = self.read_csv(csv_filename)

        # Copiar dataframe
        df = df_raw.copy(deep=True)
        
        # Convertir a booleano
        
        # Reemplazo con infer_objects para evitar advertencias
        df[list(self.valores.keys())] = df[list(self.valores.keys())].replace({'TRUE': True, 'FALSE': False}).infer_objects()


        

        
        # Obtener las unidades
        df['unidad'] = df.apply(lambda row: next((self.regimen[key] for key in self.regimen.keys() if key in row and row[key] == True), None), axis=1)
        
        # Obtener los valores
        df['valor'] = df.apply(lambda row: next((self.valores[key] for key in self.valores.keys() if key in row and row[key] == True), None), axis=1)
        
        # Quitar planes
        df = df[df['Tipo'] != 'Plan']
        
        # Mantener solo las columnas necesarias
        columns = ['Plan', 'Accion', 'Trabajo', 'Actividad', 'Tipo', 'Parada', 'Relevancia', 'Especialidad', 'valor', 'unidad']
        df = df[columns]
        
        # Crear la nueva columna fk_activity que tendrá relaciones con las actividades padre
        df['fk_activity'] = None
        df['fkc_regime'] = None

        # Renombrar los nombres de las columnas
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

        # Mantener las columnas del excel en el orden indicado
        columnas_excel = ['fk_activity', 'fk_plan', 'fk_action', 'name', 'fkc_activity_type', 'fkc_priority', 'fk_specialty', 'fkc_regime', 'stoppage', 'time_interval_value', 'fk_periodicity_unit']
        df = df[columnas_excel]

        # Filtrar las columnas necesarias para obtener los valores únicos
        self.df_plan = self.get_unique(df, "fk_plan")
        self.df_action = self.get_unique(df, "fk_action")
        self.df_speciality = self.get_unique(df, "fk_specialty")

        # Filtrar los datos de "Actividad" y "Tarea"
        filtered_data = df[(df['fkc_activity_type'] == 'Actividad') | (df['fkc_activity_type'] == 'Tarea')]

        # Asignar fk_activity para las tareas basándose en su actividad padre
        parent_index = None
        for i, row in filtered_data.iterrows():
            if row['fkc_activity_type'] == 'Actividad':
                parent_index = i
            elif row['fkc_activity_type'] == 'Tarea':
                filtered_data.at[i, 'fk_activity'] = parent_index

        # Asignar valores de fk_plan, fk_action y fk_specialty
        filtered_data['fk_plan'] = filtered_data['fk_plan'].apply(lambda x: self.buscar(self.df_plan, x))
        filtered_data['fk_action'] = filtered_data['fk_action'].apply(lambda x: self.buscar(self.df_action, x))
        filtered_data['fk_specialty'] = filtered_data['fk_specialty'].apply(lambda x: self.buscar(self.df_speciality, x))

        return filtered_data

    def get_unique(self, df: pd.DataFrame, column: str):
        """
        Obtiene un DataFrame con valores únicos de la columna especificada y ajusta los índices.

        Args:
            df (pd.DataFrame): El DataFrame a procesar.
            column (str): El nombre de la columna para la cual obtener los valores únicos.

        Returns:
            pd.DataFrame: Un DataFrame con valores únicos y un índice ajustado.
        """
        df[column] = df[column].str.strip()
        df = df[df[column].notnull()]
        df_unique = pd.DataFrame(df[column].unique(), columns=['value'])
        df_unique.index = df_unique.index + 1
        return df_unique

    def buscar(self, df: pd.DataFrame, valor, columna="value"):
        """
        Busca un valor específico en una columna del DataFrame y retorna su índice.

        Args:
            df (pd.DataFrame): El DataFrame en el cual buscar.
            valor (any): El valor a buscar.
            columna (str): El nombre de la columna en la cual realizar la búsqueda.

        Returns:
            int: El índice del valor encontrado.
        """
        return df[df[columna] == valor].index[0]
    def save_to_excel(self, output_path):
        with pd.ExcelWriter(output_path) as writer:
            self.filtered_data.to_excel(writer, sheet_name='filtered_data', index=False)
            self.df_plan.to_excel(writer, sheet_name='df_plan', index=False)
            self.df_action.to_excel(writer, sheet_name='df_action', index=False)
            self.df_speciality.to_excel(writer, sheet_name='df_speciality', index=False)


sheet_url = "https://docs.google.com/spreadsheets/d/1OkECu7qNfGZxX_rc2RDbaz0A-oE_gUwJ0P2tjU_x-q0/edit?gid=1199302294#gid=1199302294"
file_path = "temp_sheet.csv"  # Puedes cambiar el nombre del archivo si lo deseas
processor = GoogleSheetProcessor(sheet_url, file_path)
filtered_data = processor.process_data()
processor.save_to_excel("output.xlsx")

# Mostrar el resultado
print(filtered_data)

