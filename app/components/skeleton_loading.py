import streamlit as st

class SkeletonLoading:
    def __init__(self):
        pass

    @staticmethod
    def render():
        # Placeholder para información del paciente
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Datos Personales")
            for _ in range(6):
                st.markdown("▒▒▒▒▒▒▒▒▒▒▒▒")
        
        with col2:
            st.subheader("Atributos Físicos")
            for _ in range(4):
                st.markdown("▒▒▒▒▒▒▒▒▒▒▒▒")
        
        with col3:
            st.subheader("Estancia Hospitalaria")
            for _ in range(4):
                st.markdown("▒▒▒▒▒▒▒▒▒▒▒▒")
