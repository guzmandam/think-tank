import streamlit as st

class PatientPrescriptions:
    def __init__(self, prescriptions):
        self.prescriptions = prescriptions

    def render(self):
        st.header("Prescripciones")
        st.dataframe(self.prescriptions, use_container_width=True)