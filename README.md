# Extractor de datos del paciente

## Descripción

Esta aplicación permite extraer los datos de un paciente de diferentes archivos PDF y mostrar un resumen de los mismos en la pagina con la posibilidad de descargar el historial de medicamentos en formato CSV.

## Como correr la aplicación

Para correr la aplicación se debe tener instalado Python 3.9 o superior. Luego se deben instalar las dependencias del proyecto con el siguiente comando:

```bash
pip install -r requirements.txt
```

Una vez instaladas las dependencias se puede correr la aplicación con el siguiente comando:

```bash
streamlit run ./app/app.py
```