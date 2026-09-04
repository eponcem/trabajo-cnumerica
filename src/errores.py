import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv

def redondear_cifras(x, cifras=2):
    if x == 0:
        return 0.0
    return float(f"{x:.{cifras}g}")

v_redondear = np.vectorize(redondear_cifras)

def escribir_seccion_csv(ruta, modo, titulo, cabecera, filas):
    with open(ruta, modo, newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow([titulo])
        escritor.writerow(cabecera)
        for fila in filas:
            escritor.writerow(fila)
        escritor.writerow([])

