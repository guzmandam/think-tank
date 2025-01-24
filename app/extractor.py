# Import utility functions to avoid code duplication
from utils import (
    generate_fake_signal_data,
    get_patient_data,
    get_notes_data,
    get_medicamentos
)

from enum import Enum
from typing import Union, List, Dict
from time import sleep

import pandas as pd
from PyPDF2 import PdfReader

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
        # File paths
        self.file_paths: List = file_paths
        
        # Raw sections (Sections)
        self.footer_header_section_raw: List[str] = []

        # Personal Info
        self.names: str = ""
        self.fathern_lastname: str = ""
        self.mothern_lastname: str = ""
        self.birth_date: str = "" # "YYYY-MM-DD"
        self.sex: Union[Sex, str] = ""
        self.age: str = ""
        self.him: str = ""
        self.expedient: str = ""
        
        # Other patient information
        self.weight: float = 0.0
        self.height: float = 0.0
        self.allergies: Allergies = ""
        self.allergies_description: str = ""
        self.entry_date: str = "" # "YYYY-MM-DD"
        self.discharge_date: str = "" # "YYYY-MM-DD"
        self.stay_days: int = 0
        self.base_final_diagnosis: str = ""
        self.service: str = ""

        # Information in tables
        self.notes: List[Dict] = []
        self.prescriptions: Union[pd.DataFrame, List[Dict]] = [] # List of dictionaries or DataFrame
        self.diagnosis: Union[pd.DataFrame, List[Dict]] = [] # List of dictionaries or DataFrame
        self.vital_signs: pd.DataFrame = pd.DataFrame()
    
    def get_raw_sections(self):
        for file_path in self.file_paths:
            reader = PdfReader(file_path)
            raw_header_footer = reader.pages[0].extract_text().split("\n")
            
            self.footer_header_section_raw.append(
                "\n".join(raw_header_footer[-6:])
            )
    
    def convert_to_dataframe(self):
        """
        Convert the list of dictionaries to a DataFrame
        """
        if isinstance(self.prescriptions, list):
            self.prescriptions = pd.DataFrame(self.prescriptions)

        if isinstance(self.diagnosis, list):
            self.diagnosis = pd.DataFrame(self.diagnosis)

    def generate_patient_info(self):
        sleep(2) # Simulate a delay

        # Generate patient information (fake)
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

        self.vital_signs = generate_fake_signal_data()
        
    def extract_personal_info(self):
        personal_info = get_patient_data(self.footer_header_section_raw[0])
        
        self.names = personal_info.get("Nombres", "")
        self.fathern_lastname = personal_info.get("ApellidoPaterno", "")
        self.mothern_lastname = personal_info.get("ApellidoMaterno", "")
        self.birth_date = personal_info.get("FechaNacimiento", "")
        self.sex = personal_info.get("Sexo", "")
        self.age = personal_info.get("Edad", "")
        self.him = personal_info.get("HIM", "")
        self.expedient = personal_info.get("Expediente", "")
    
    def extract_notes_info(self):
        notes_conv = []
        
        for file_raw_footer_header in self.footer_header_section_raw:
            note = get_notes_data(file_raw_footer_header)
            notes_conv.append(note)
        
        self.notes = pd.DataFrame(notes_conv)
        
    def extract_prescriptions(self):
        self.prescriptions = get_medicamentos(self.file_paths)
        
    def extract(self):
        # Load the raw sections
        self.get_raw_sections()
        
        # Actual extraction of data
        self.extract_personal_info()
        self.extract_notes_info()
        self.extract_prescriptions()
        
        # Dummy data for the rest of the sections
        self.generate_patient_info()
    
    def __str__(self):
        return f"Paciente: {self.name} - ID: {self.id}"
    
    def __repr__(self):
        return self.__str__()