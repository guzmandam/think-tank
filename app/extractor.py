# Import utility functions to avoid code duplication
from utils import (
    generate_fake_signal_data
)

from enum import Enum
from typing import Union, List, Dict
from time import sleep

import pandas as pd

class Sex(Enum):
    MALE = "masculino"
    FEMALE = "femenino"
    OTHER = "otro"

class Allergies(Enum):
    YES = "si"
    NO = "no"

class PatientDataExtractor:
    """
    Class to extract data from a file
    - file_path: str, path to the file

    Given a file path, this class will extract patient data from the files
    """
    def __init__(self, file_paths):
        self.file_paths = file_paths

        self.name: str = ""
        self.id: str = ""
        self.tank_number: int = 0
        self.calculated_age_days: int = 0
        self.birth_date: str = "" # "YYYY-MM-DD"
        self.age_days: int = 0
        self.age_months: int = 0
        self.age_years: int = 0
        self.sex: Sex = ""
        self.weight: float = 0.0
        self.height: float = 0.0
        self.allergies: Allergies = ""
        self.allergies_description: str = ""
        self.entry_date: str = "" # "YYYY-MM-DD"
        self.discharge_date: str = "" # "YYYY-MM-DD"
        self.stay_days: int = 0
        self.base_final_diagnosis: str = ""
        self.service: str = ""

        self.prescriptions: Union[pd.DataFrame, List[Dict]] = [] # List of dictionaries or DataFrame
        self.diagnosis: Union[pd.DataFrame, List[Dict]] = [] # List of dictionaries or DataFrame
        self.vital_signs: pd.DataFrame = pd.DataFrame()
    
    def convert_to_dataframe(self):
        """
        Convert the list of dictionaries to a DataFrame
        """
        if isinstance(self.prescriptions, list):
            self.prescriptions = pd.DataFrame(self.prescriptions)

        if isinstance(self.diagnosis, list):
            self.diagnosis = pd.DataFrame(self.diagnosis)

    def generate_patient_info(self):
        sleep(5) # Simulate a delay

        # Generate patient information (fake)
        self.name = "Juan Pérez García"
        self.id = "PAC-2024-001"
        self.tank_number = 123
        self.birth_date = "2000-03-15"
        self.age_days = 200
        self.age_months = 288
        self.age_years = 24
        self.sex = Sex.MALE
        self.weight = 70.0
        self.height = 1.75
        self.allergies = Allergies.YES
        self.allergies_description = "Alergia a la penicilina"
        self.entry_date = "2024-03-15"
        self.discharge_date = "2024-03-20"
        self.stay_days = 5
        self.base_final_diagnosis = "Neumonía"
        self.diagnosis = "Neumonía adquirida en la comunidad"
        self.service = "Medicina Interna"

        self.prescriptions = [
            {
                "nombre": "Paracetamol",
                "dosis": 500,
                "unidades": "mg",
                "indicaciones": "Tomar cada 8 horas",
                "via_administracion": "VO",
                "fecha_inicio": "2024-03-15",
                "fecha_termino": "2024-03-20",
                "ajuste_dosis": "No aplica"
            },
            {
                "nombre": "Amoxicilina",
                "dosis": 500,
                "unidades": "mg",
                "indicaciones": "Tomar cada 8 horas",
                "via_administracion": "VO",
                "fecha_inicio": "2024-03-15",
                "fecha_termino": "2024-03-20",
                "ajuste_dosis": "No aplica"
            },
            {
                "nombre": "Ibuprofeno",
                "dosis": 400,
                "unidades": "mg",
                "indicaciones": "Tomar cada 8 horas",
                "via_administracion": "VO",
                "fecha_inicio": "2024-03-15",
                "fecha_termino": "2024-03-20",
                "ajuste_dosis": "No aplica"
            }
        ]

        self.diagnosis = [
            {
                "fecha": "2024-03-15",
                "nombre": "Neumonía",
                "descripcion": "Neumonía adquirida en la comunidad"
            },
            {
                "fecha": "2024-03-15",
                "nombre": "Faringitis",
                "descripcion": "Faringitis aguda"
            },
            {
                "fecha": "2024-03-15",
                "nombre": "Rinitis",
                "descripcion": "Rinitis alérgica"
            },
            {
                "fecha": "2024-03-15",
                "nombre": "Otitis",
                "descripcion": "Otitis media"
            }
        ]

        self.convert_to_dataframe()

        self.vital_signs = generate_fake_signal_data()

    def extract(self):
        """
        Extract data from the file

        Returns:
        - data: DataFrame
            - Columns: [
                "nombre": <str> nombre del medicamento,
                "dosis": <int> dosis del medicamento, 
                "unidades": <str> unidades del medicamento (mg, ml, etc),
                "indicaciones": <str> indicaciones del medicamento,
                "via_administracion": <str> vía de administración del medicamento (IV, VO),
                "fecha_inicio": <datetime> fecha de inicio del medicamento,
                "fecha_termino": <datetime> fecha de término del medicamento,
                "ajuste_dosis": <str> ajuste de dosis del medicamento,
            ]
        """
        data = ... # Extract data from the file
        self.prescriptions = data
    
    def __str__(self):
        return f"Paciente: {self.name} - ID: {self.id}"
    
    def __repr__(self):
        return self.__str__()