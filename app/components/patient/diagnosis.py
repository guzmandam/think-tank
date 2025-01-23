import streamlit as st

class PatientDiagnosis:
    def __init__(self, diagnosis_table):
        self.diagnosis_table = diagnosis_table
    
    def render(self):
        st.header("Diagnósticos")
        st.dataframe(self.diagnosis_table, use_container_width=True)