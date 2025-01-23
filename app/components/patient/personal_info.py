import streamlit as st

class PatientInfo:
    def __init__(self, patient):
        self.patient = patient
    
    def render(self):
        st.header("Información del Paciente")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Datos Personales")
            st.markdown(f"**Nombre:** {self.patient.name}")
            st.markdown(f"**ID:** {self.patient.id}")
            st.markdown(f"**Número de Tanque:** {self.patient.tank_number}")
            st.markdown(f"**Fecha de Nacimiento:** {self.patient.birth_date}")
            st.markdown(f"**Edad:** {self.patient.age_years} años, {self.patient.age_months} meses, {self.patient.age_days} días")
            st.markdown(f"**Sexo:** {self.patient.sex.value.capitalize()}")

        with col2:
            st.subheader("Atributos Físicos")
            st.markdown(f"**Peso:** {self.patient.weight} kg")
            st.markdown(f"**Altura:** {self.patient.height} m")
            st.markdown(f"**Alergias:** {self.patient.allergies.value.capitalize()}")
            st.markdown(f"**Descripción de Alergias:** {self.patient.allergies_description}")

        with col3:
            st.subheader("Estancia Hospitalaria")
            st.markdown(f"**Fecha de Ingreso:** {self.patient.entry_date}")
            st.markdown(f"**Fecha de Alta:** {self.patient.discharge_date}")
            st.markdown(f"**Días de Estancia:** {self.patient.stay_days} días")
            st.markdown(f"**Servicio:** {self.patient.service}")