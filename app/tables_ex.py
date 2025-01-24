from PyPDF2 import PdfReader
import pandas as pd
import re

def pdf_a_texto(ruta):
    reader = PdfReader(ruta)
    documento = ""
    for pagina in range(len(reader.pages)):
        documento = documento + reader.pages[pagina].extract_text()
    return documento

#secciones = ["Signos Vitales", "Diagnósticos Activos", "Órdenes de Dietéticas Activas", "Órdenes de Enfermería Activas", "Órdenes de Medicamentos Hospitalarios"] 

def extract_tables_from_routes(rutas, seccion):
    tablas = []

    for ruta in rutas:
        documento = pdf_a_texto(ruta)
        df = extraer_tabla(documento, seccion)
        tablas.append(df)

    df_ejemplo =  pd.concat(tablas, ignore_index=True)
    
    return df_ejemplo.drop_duplicates().reset_index(drop=True)

def extract_fecha(renglon):
    fecha = ""
    for n in range(17):
        fecha = fecha + renglon[n]  
    return fecha[:-1]
    
def econtrar_seccion(lst, seccion):
    Bandera = False
    lst_resultado = []
    for i in lst:
        if(Bandera):
            if(i == ' '):
                Bandera = False
            else:
                date_pattern = re.compile(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}")
                match = date_pattern.search(i)
                if not(match is None):
                    lst_resultado.append(i)
                else:
                    n = lst.index(i)
                    match1 = date_pattern.search(lst[n-1])
                    match2 = date_pattern.search(lst[n+1])
                    if ((not(match1 is None))&(not(match2 is None))):
                        lst_resultado.pop()
        if (i.startswith(seccion)):
            Bandera = True
    return lst_resultado
    
def eliminar_ruido(lst):
    lista_guardado = []
    lista_resultado = []
    elemento_append = True
    for renglon in lst:
        if (renglon.startswith("Expediente:"))|("Derechos de Autor" in renglon):
            elemento_append = not(elemento_append)
            if ("Derechos de Autor" in renglon):
                lista_guardado.append(not(elemento_append))
            else:
                lista_guardado.append(elemento_append)
        else:
            lista_guardado.append(elemento_append)
    for i in range(len(lst)):
        if lista_guardado[i]:
            lista_resultado.append(lst[i])
    return lista_resultado
    
def comprobacion_final(tabla, columnas):
    No_Valido = False
    for i in tabla:
        if len(i) != len(columnas):
            No_Valido = True
    if No_Valido:
        df = pd.DataFrame(columns=columnas)
    else:
        df = pd.DataFrame(tabla, columns=columnas)   
    return df

def extraer_tabla(documento_txt, nombre_seccion):
    
    lst_documento = documento_txt.split('\n')
    lst_documento = eliminar_ruido(lst_documento)
    tabla_seccion = econtrar_seccion(lst_documento, "Órdenes de Dietéticas Activas")
    
    match nombre_seccion:
        case "Signos Vitales":
            columns = ['Fecha/Hora', 'FR', 'FC', 'PAS', 'PAD', 'SAT O2', 'Temp °C', 'Peso', 'Talla']
            tabla_seccion = econtrar_seccion(lst_documento, "Signos Vitales")
            tabla = []
            for i in tabla_seccion:
                if (not(i.startswith('Fecha/Hora'))):
                    datos = []
                    fecha = extract_fecha(i)
                    datos.append(fecha)
                    fecha = fecha + " "
                    tmp_string = i.replace(fecha, '')
                    lista_dividida = tmp_string.split('   ')
                    lista_dividida.pop()
                    datos.extend(lista_dividida)
                    tabla.append(datos)
            df = comprobacion_final(tabla, columns)
            return df
        case "Órdenes de Dietéticas Activas":
            columns = ['Fecha Ingresada', 'Tipo', 'Tipo Terapéutico', 'Notas']
            tabla_seccion = econtrar_seccion(lst_documento, "Órdenes de Dietéticas Activas")
            tabla = []
            for i in tabla_seccion:
                if (not(i.startswith('Fecha'))):
                    datos = []
                    fecha = extract_fecha(i)
                    datos.append(fecha)
                    fecha = fecha + " "
                    tmp_string = i.replace(fecha, '')
                    lista_dividida = tmp_string.split('   ')
                    lista_dividida.pop()
                    datos.extend(lista_dividida)
                    tabla.append(datos)

            df = comprobacion_final(tabla, columns)
            return df
        case "Diagnósticos Activos":
            columns = ['Fecha Ingresada', 'Descripción', 'Tipo', 'Médico', 'Notas']
            tabla_seccion = econtrar_seccion(lst_documento, "Diagnósticos Activos")
            tabla = []
            for i in tabla_seccion:
                if (not(i.startswith('Fecha'))):
                    datos = []
                    fecha = extract_fecha(i)
                    datos.append(fecha)
                    fecha = fecha + " "
                    tmp_string = i.replace(fecha, '')
                    lista_dividida = tmp_string.split('   ')
                    lista_dividida.pop()
                    datos.append(lista_dividida[0])
                    datos.append(lista_dividida[1])
                    datofinal = lista_dividida[-1]
                    lista_dividida.pop(0)
                    lista_dividida.pop(0)
                    lista_dividida.pop()
                    cadena = ""
                    for elemento in lista_dividida:
                        cadena = cadena + elemento
                    datos.append(cadena)
                    datos.append(datofinal)
                    tabla.append(datos)
            df = comprobacion_final(tabla, columns)
            return df
        case "Órdenes de Enfermería Activas":
            columns = ['Fecha Ingresada', 'Orden', 'Médico']
            tabla_seccion = econtrar_seccion(lst_documento, "Órdenes de Enfermería Activas")
            tabla = []
            for i in tabla_seccion:
                if (not(i.startswith('Fecha'))):
                    datos = []
                    fecha = extract_fecha(i)
                    datos.append(fecha)
                    fecha = fecha + " "
                    tmp_string = i.replace(fecha, '')
                    lista_dividida = tmp_string.split('   ')
                    lista_dividida.pop()
                    datos.append(lista_dividida[0])
                    lista_dividida.pop(0)
                    cadena = ""
                    for elemento in lista_dividida:
                        cadena = cadena + elemento      
                    datos.append(cadena)
                    tabla.append(datos)
            df = comprobacion_final(tabla, columns)            
            return df
        case "Órdenes de Medicamentos Hospitalarios":
            columns = ["Inicio", "Medicamento", "Frecuencia", "Via", "Dosis", "UDM", "Cantidad", "Tipo", "Médico", "Tasa de Flujo"]
            tabla_seccion = econtrar_seccion(lst_documento, "Órdenes de Medicamentos Hospitalarios")
            tabla = []
            for i in tabla_seccion:
                if (not(i.startswith('Inicio'))):
                    datos = []
                    fecha = extract_fecha(i)
                    datos.append(fecha)
                    fecha = fecha + " "
                    tmp_string = i.replace(fecha, '')
                    lista_dividida = tmp_string.split('   ')
                    lista_dividida.pop()
                    datofinal = lista_dividida[-1]
                    lista_dividida.pop()
                    for _ in range(7):
                        datos.append(lista_dividida[0])
                        lista_dividida.pop(0)
                    cadena = ""
                    for elemento in lista_dividida:
                        cadena = cadena + elemento
                    datos.append(cadena)
                    datos.append(datofinal)
                    tabla.append(datos)
            df = comprobacion_final(tabla, columns)
            return df
        case _:
            df = pd.DataFrame()           
            return df
                   
