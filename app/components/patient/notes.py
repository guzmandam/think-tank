import streamlit as st

class PatientNotes:
    def __init__(self, notes_table):
        self.notes_table = notes_table
        
    def render(self):
        st.header("Notas del Paciente")
        st.dataframe(self.notes_table, use_container_width=True)