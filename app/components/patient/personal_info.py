import streamlit as st

class PatientInfo:
    def __init__(self, patient):
        self.patient = patient
    
    def render(self):
        st.header("Información del Paciente")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Datos Personales")
            st.markdown(f"**Nombres:** {self.patient.names}")
            st.markdown(f"**Apellido Paterno:** {self.patient.fathern_lastname}")
            st.markdown(f"**Apellido Materno:** {self.patient.mothern_lastname}")
            st.markdown(f"**HIM:** {self.patient.him}")
            st.markdown(f"**Expediente:** {self.patient.expedient}")
            st.markdown(f"**Fecha de Nacimiento:** {self.patient.birth_date}")
            st.markdown(f"**Edad:** {self.patient.age}")
            st.markdown(f"**Sexo:** {self.patient.sex.capitalize()}")

        with col2:
            st.subheader("Atributos Físicos")
            st.markdown(f"**Peso:** {self.patient.weight} kg")
            st.markdown(f"**Altura:** {self.patient.height} m")
            st.markdown(f"**Alergias:** {self.patient.allergies.value.capitalize()}")
            st.markdown(f"**Descripción de Alergias:** {self.patient.allergies_description}")