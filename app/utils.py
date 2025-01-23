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