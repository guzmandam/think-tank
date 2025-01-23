from utils import show_skeleton_loading
from extractor import PatientDataExtractor

import streamlit as st

st.set_page_config(page_title="Panel del Paciente", layout="wide")

st.title("Extracción de Datos de Pacientes")

# CSS personalizado para centrar la tabla
st.markdown("""
    <style>
        .stDataFrame {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Suba los archivos PDF aquí")

uploaded_files = st.file_uploader(
    "Elija un archivo PDF", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    patient = PatientDataExtractor(uploaded_files)

    placeholder = st.empty()

    with placeholder.container():
        show_skeleton_loading()
        patient.generate_patient_info() # Delay / Simulate loading

    with placeholder.container():
        st.title("Panel del Paciente")
        st.markdown("---")

        st.header("Información del Paciente")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Datos Personales")
            st.markdown(f"**Nombre:** {patient.name}")
            st.markdown(f"**ID:** {patient.id}")
            st.markdown(f"**Número de Tanque:** {patient.tank_number}")
            st.markdown(f"**Fecha de Nacimiento:** {patient.birth_date}")
            st.markdown(f"**Edad:** {patient.age_years} años, {patient.age_months} meses, {patient.age_days} días")
            st.markdown(f"**Sexo:** {patient.sex.value.capitalize()}")

        with col2:
            st.subheader("Atributos Físicos")
            st.markdown(f"**Peso:** {patient.weight} kg")
            st.markdown(f"**Altura:** {patient.height} m")
            st.markdown(f"**Alergias:** {patient.allergies.value.capitalize()}")
            st.markdown(f"**Descripción de Alergias:** {patient.allergies_description}")

        with col3:
            st.subheader("Estancia Hospitalaria")
            st.markdown(f"**Fecha de Ingreso:** {patient.entry_date}")
            st.markdown(f"**Fecha de Alta:** {patient.discharge_date}")
            st.markdown(f"**Días de Estancia:** {patient.stay_days} días")
            st.markdown(f"**Servicio:** {patient.service}")

        st.markdown("---")

        st.header("Diagnóstico")
        st.markdown(f"**Diagnóstico Base Final:** {patient.base_final_diagnosis}")
        st.markdown(f"**Diagnóstico:** {patient.diagnosis}")

        st.markdown("---")

        st.header("Prescripciones")
        prescriptions_df = st.dataframe(patient.prescriptions, use_container_width=True)

        st.markdown("---")
        st.markdown("**Nota:** Este es un panel de paciente demostrativo con fines educativos.")