# Extractor de datos del paciente

## Descripción

Esta aplicación permite extraer los datos de un paciente de diferentes archivos PDF y mostrar un resumen de los mismos en la pagina con la posibilidad de descargar el historial de medicamentos en formato CSV.

## Como correr la aplicación

Para correr la aplicación se debe tener instalado Docker. Luego se debe ejecutar el siguiente comando en la raíz del proyecto:

```bash
docker build -t think-tank-team1 .
```

Luego se debe ejecutar el siguiente comando:

```bash
docker run -p 3000:3000 think-tank-team1
```

Finalmente se debe abrir el navegador y acceder a la siguiente URL:

```bash
http://localhost:3000/
```