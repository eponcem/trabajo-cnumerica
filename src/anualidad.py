import numpy as np
import os
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv
from errores import v_redondear, escribir_seccion_csv

def analizar_cancelacion_a3(valores, directorio):
    v22 = valores[11]
    v23 = valores[23]
    
    aprox22 = v_redondear(v22, 3) 
    aprox23 = v_redondear(v23, 3)
    
    ea22 = np.abs(v22 - aprox22)
    ea23 = np.abs(v23 - aprox23)
    
    delta_a3 = aprox23 - aprox22
    ea_delta_a3 = ea22 + ea23 
    er_delta_a3 = (ea_delta_a3 / np.abs(delta_a3)) * 100

    afirmacion_segura = bool(np.abs(delta_a3) > ea_delta_a3)

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(ruta_csv, 'a','--- A3: cancelacion diciembre 2022 vs diciembre 2023 (3 cifras significativas) ---',
        ['delta_p', 'error_absoluto', 'error_relativo_pct', 'afirmacion_segura'], [[round(delta_a3, 2), round(ea_delta_a3, 2), round(er_delta_a3, 2), afirmacion_segura]],)

