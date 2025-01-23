from extractor import PatientDataExtractor

from components.patient.personal_info import PatientInfo
from components.patient.diagnosis import PatientDiagnosis
from components.patient.prescriptions import PatientPrescriptions
from components.patient.vital_signs import PatientVitalSigns

from components.skeleton_loading import SkeletonLoading

import streamlit as st

st.set_page_config(page_title="Panel del Paciente", layout="wide")

st.markdown(f"<h1 style='text-align: center;'>Extracción de Datos de Pacientes</h1>", unsafe_allow_html=True)

# CSS personalizado para centrar la tabla
st.markdown("""
    <style>
        .stDataFrame {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

st.subheader("Suba los archivos PDF aquí")

uploaded_files = st.file_uploader(
    "Elija un archivo PDF", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    patient = PatientDataExtractor(uploaded_files)

    placeholder = st.empty()

    with placeholder.container():
        st.title("Panel del Paciente")
        SkeletonLoading().render()
        patient.generate_patient_info() # Delay / Simulate loading

    with placeholder.container():
        st.title("Panel del Paciente")

        tabs = st.tabs(["Información del Paciente", "Diagnósticos", "Prescripciones", "Signos Vitales"])

        with tabs[0]:
            patient_info = PatientInfo(patient)
            patient_info.render()

        with tabs[1]:
            patient_diagnosis = PatientDiagnosis(patient.diagnosis)
            patient_diagnosis.render()

        with tabs[2]:
            patient_prescriptions = PatientPrescriptions(patient.prescriptions)
            patient_prescriptions.render()

        with tabs[3]:
            patient_vital_signs = PatientVitalSigns(patient.vital_signs)
            patient_vital_signs.render()

        st.markdown("---")
        st.markdown("**Nota:** Este es un panel de paciente demostrativo con fines educativos.")