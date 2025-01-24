import pandas as pd
import numpy as np

import re

from tables_ex import extract_tables_from_routes

def util_example():
    return "This is a utility function"

def generate_fake_signal_data(days=30):
    dates = pd.date_range(start='2023-10-01', periods=days, freq='D')
    vital_signs = pd.DataFrame({
        'Fecha': dates,
        'Temperatura (°C)': np.round(np.random.normal(loc=36.5, scale=0.5, size=30), 1),
        'Leucocitos (total)': np.random.randint(4000, 11000, size=30),
        'Saturación (%)': np.random.randint(92, 100, size=30),
        'Frecuencia Cardiaca (total)': np.random.randint(60, 100, size=30),
        'Frecuencia Respiratoria (total)': np.random.randint(12, 20, size=30),
        'Bandas (%)': np.round(np.random.uniform(0, 10, size=30), 1)
    })

    return vital_signs

def resample_data(data, time_scale="Dia"):
    """Resample data based on selected time scale"""
    scale_map = {
        'Dia': 'D',
        'Semana': 'W',
        'Mes': 'M'
    }
    
    data = data.copy()
    data['Fecha'] = pd.to_datetime(data['Fecha'])
    data = data.set_index('Fecha')
    resampled = data.resample(scale_map[time_scale]).mean()
    return resampled.reset_index()

def capitalize_first_letter(text):
    return ' '.join([word.capitalize() for word in text.split()])

def get_patient_data(text):
    """
    Extracts patient data such as full name, birth date, gender, and age from the given text
    and appends the information to the provided DataFrame. The column names will be added
    to the first row of the DataFrame.

    Parameters:
    text (str): The input text containing patient information.
    df (pd.DataFrame): The existing DataFrame to which the extracted data will be added.

    Returns:
    pd.DataFrame: Updated DataFrame with the extracted patient data, with column names
                  added as the first row.
    """

    # Extract the full name by replacing the HIM number with "Nombre Completo" in the text
    re_him = r"HIM:\s*([\d]+)"
    new_header = re.sub(re_him, r" Nombre Completo: ", text)
    re_name =  r"Nombre Completo:\s*(.*?)Fecha"
    name_match = re.findall(re_name, new_header)
    full_name = capitalize_first_letter(name_match[0]) if name_match else None

    # Split the full name into father's last name, mother's last name, and given names
    if full_name:
        father_last_name = full_name.split()[0]
        mother_last_name = full_name.split()[1].replace(",","")
        names = " ".join(full_name.split()[2:])
    else:
        father_last_name, mother_last_name, names = None, None, None

    # Extract birth date in the format DD/MM/YYYY
    re_birth_date = r"Fecha de Nacimiento:\s*(\d{2}/\d{2}/\d{4})"
    birth_date_match = re.findall(re_birth_date, text)
    birth_date = birth_date_match[0] if birth_date_match else None

    # Extract gender (Sexo)
    re_sex = r"\b(Femenino|Masculino)\b"
    sex_match = re.findall(re_sex, text)
    sex = sex_match[0] if sex_match else None

    # Extract age (inside parentheses)
    re_age = r"\((.*?)\)"
    age_match = re.findall(re_age, text)
    age = age_match[0] if age_match else None
    
    # Extract 'Numero de Expediente' (Case Number)
    re_no_expediente = r"Expediente:\s*([\d]+)"
    no_expediente_match = re.findall(re_no_expediente, text)
    no_expediente = no_expediente_match[0] if no_expediente_match else None

    # Extract 'HIM' identifier
    re_him = r"HIM:\s*([\d]+)"
    him_match = re.findall(re_him, text)
    him = him_match[0] if him_match else None

    # Add extracted data to the DataFrame
    new_data = {
        'ApellidoPaterno': father_last_name,
        'ApellidoMaterno': mother_last_name,
        'Nombres': names,
        'FechaNacimiento': birth_date,
        'Sexo': sex,
        'Edad': age,
        'Expediente': no_expediente,
        'HIM': him
    }
    
    return new_data

def get_notes_data(text):
    """
    Extracts medical information from the given text and updates the first row of the DataFrame.
    If new columns do not exist in the DataFrame, they will be added.

    Parameters:
    text (str): The input text containing medical information.
    df (pd.DataFrame): The existing DataFrame to which the extracted data will be added.

    Returns:
    pd.DataFrame: Updated DataFrame with the extracted medical data in the first row.
    """

    # Extract the hospital admission date
    re_entry_date = r"Fecha de Ingreso:\s*(\d{2}/\d{2}/\d{4})"
    entry_date_match = re.findall(re_entry_date, text)
    entry_date = entry_date_match[0] if entry_date_match else None

    # Extract the hospital admission time
    re_entry_time = r"Fecha de Ingreso:\s*(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})"
    entry_time_match = re.findall(re_entry_time, text)
    entry_time = entry_time_match[0][1] if entry_time_match else None

    # Extract the hospital discharge date
    re_discharge_date = r"Dado de Alta:\s*(\d{2}/\d{2}/\d{4})"
    discharge_date_match = re.findall(re_discharge_date, text)
    discharge_date = discharge_date_match[0] if discharge_date_match else None

    # Extract the hospital discharge time
    re_discharge_time = r"Dado de Alta:\s*(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})"
    discharge_time_match = re.findall(re_discharge_time, text)
    discharge_time = discharge_time_match[0][1] if discharge_time_match else None

    # Extract the doctor's name who signed the medical note
    re_dc_name = r"Firmado por:\s*(.*?)-"
    dc_name_match = re.findall(re_dc_name, text)
    dc_name = dc_name_match[0] if dc_name_match else None
    # Quitamos espacios extras
    dc_name = re.sub(r'\s+', ' ', dc_name).strip()
    dc_name = capitalize_first_letter(dc_name)

    # Extract the doctor's professional license number
    re_dc_number =  r"PROF.:\s*([\d]+)"
    dc_number_match = re.findall(re_dc_number, text)
    dc_number = dc_number_match[0] if dc_number_match else None

    # Extract the creation date of the medical note
    new_header = re.sub(re_dc_name, r"Creacion: ", text)

    re_creation_date = r"Creacion:\s*(\d{2}/\d{2}/\d{4})"
    creation_date_match = re.findall(re_creation_date, new_header)
    creation_date = creation_date_match[0] if creation_date_match else None

    # Extract the creation time of the medical note
    re_creation_time = r"Creacion:\s*(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})"
    creation_time_match = re.findall(re_creation_time, new_header)
    creation_time = creation_time_match[0][1] if creation_time_match else None

    # Extract the hospital name
    re_hospital_name = r"Hospital\s*(.*?)\n"
    hospital_name_match = re.findall(re_hospital_name, text)
    hospital_name = "Hospital " + hospital_name_match[0] if hospital_name_match else None
    
    # Extract 'Numero de Nota' (Note Number)
    re_no_nota = r"\nNo.\s*([\d]+)"
    no_nota_match = re.findall(re_no_nota, text)
    no_nota = no_nota_match[0] if no_nota_match else None

    # Extract 'Tipo de Nota' (second line in the text)
    lines = text.splitlines()
    tipo_nota = lines[1] if len(lines) > 1 else None

    # Add extracted data
    new_data = {
        'FechaIngreso': entry_date,
        'HoraIngreso': entry_time,
        'FechaAlta': discharge_date,
        'HoraAlta': discharge_time,
        'FirmadoPor': dc_name,
        'CedulaProfesional': dc_number,
        'FechaCreacion': creation_date,
        'HoraCreacion': creation_time,
        'Hospital': hospital_name,
        'NoNota': no_nota,
        'TipoNota': tipo_nota
    }

    return new_data

def get_medicamentos(rutas):
    return extract_tables_from_routes(rutas, "Órdenes de Medicamentos Hospitalarios")