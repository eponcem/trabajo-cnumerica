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

if __name__ == '__main__':
    ruta = os.path.join(os.path.dirname(__file__), '../data/dolar_observado_sii_2022_2025.csv') 
    meses, etiquetas = cargar_csv(ruta)