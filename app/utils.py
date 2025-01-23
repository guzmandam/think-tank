import streamlit as st
import pandas as pd
import numpy as np

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

def show_skeleton_loading():
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
