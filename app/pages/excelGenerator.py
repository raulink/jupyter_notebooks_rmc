import pandas as pd

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.df_plan = None
        self.df_action = None
        self.df_speciality = None
        self.filtered_data = None

    def load_excel(self):
        self.df = pd.read_excel(self.file_path)

    def process_data(self):
        self.df['valor'] = self.df['Frecuencia'].apply(lambda x: self.valores.get(x, 0))
        self.df['unidad'] = self.df['Frecuencia'].apply(lambda x: self.regimen.get(x, ''))
        

        
        # Mantener solo las columnas necesarias
        columns = ['Plan', 'Accion', 'Trabajo', 'Actividad', 'Tipo', 'Parada', 'Relevancia', 'Especialidad', 'valor', 'unidad']
        self.df = self.df[columns]
        
        # Crear la nueva columna fk_activity que tendra relaciones con las actividades padre
        self.df['fk_activity'] = None
        self.df['fkc_regime'] = None
        
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
        self.df.rename(columns=nuevos_nombres, inplace=True)
        
        # Mantener las columnas del excel en el orden indicado
        columnas_excel = ['fk_activity', 'fk_plan', 'fk_action', 'name', 'fkc_activity_type', 'fkc_priority', 'fk_specialty', 'fkc_regime', 'stoppage', 'time_interval_value', 'fk_periodicity_unit']
        self.df = self.df[columnas_excel]
        
        self.df_plan = self.get_unique(self.df, "fk_plan")
        self.df_action = self.get_unique(self.df, "fk_action")
        self.df_speciality = self.get_unique(self.df, "fk_specialty")
        
        # Filtrar los datos
        self.filtered_data = self.df[(self.df['fkc_activity_type'] == 'Actividad') | (self.df['fkc_activity_type'] == 'Tarea')]
        
        # Añadir columna fk_activity
        self.filtered_data['fk_activity'] = None
        
        # Asignar fk_activity para Tareas basadas en su actividad padre
        parent_index = None
        for i, row in self.filtered_data.iterrows():
            if row['fkc_activity_type'] == 'Actividad':
                parent_index = i
            elif row['fkc_activity_type'] == 'Tarea':
                self.filtered_data.at[i, 'fk_activity'] = parent_index

    def get_unique(self, df, column_name):
        return df[[column_name]].drop_duplicates().reset_index(drop=True)
    
    def save_to_excel(self, output_path):
        with pd.ExcelWriter(output_path) as writer:
            self.filtered_data.to_excel(writer, sheet_name='filtered_data', index=False)
            self.df_plan.to_excel(writer, sheet_name='df_plan', index=False)
            self.df_action.to_excel(writer, sheet_name='df_action', index=False)
            self.df_speciality.to_excel(writer, sheet_name='df_speciality', index=False)
    
    # Diccionarios originales
    valores = {
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
    
    regimen = {
        "D": 'dia',
        "S": 'semana',
        "M": 'semana',
        "MC": 'mes',
        "2M": 'mes',
        "T": 'mes',
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

