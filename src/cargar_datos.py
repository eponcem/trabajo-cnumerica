import numpy as np
import os

def cargar_csv(archivo):
    # Usamos genfromtxt para leer el csv y delimitamos con, para y hacemos que la primera fila 
    # no tome en cuenta ya que son las etiquetas de los datos
    datos = np.genfromtxt(archivo, delimiter=',', skip_header=1, usecols=(3))
    
    # Generar etiquetas de tiempo para gráficos
    etiquetas = []
    años = [2022, 2023, 2024, 2025]
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for a in años:
        for m in meses:
            etiquetas.append(f'{m}-{a}')
    
    return datos, etiquetas
