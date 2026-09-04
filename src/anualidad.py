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

def analizar_variacion_anual_a4(valores, directorio):
    idx_eneros = np.array([0, 12, 24, 36])
    idx_dic = np.array([11, 23, 35, 47])
    años = np.array([2022, 2023, 2024, 2025])
    
    v_ene = valores[idx_eneros]
    v_dic = valores[idx_dic]
    
    aprox_ene = v_redondear(v_ene, 2)
    aprox_dic = v_redondear(v_dic, 2)
    
    ea_ene = np.abs(v_ene - aprox_ene)
    ea_dic = np.abs(v_dic - aprox_dic)
    
    deltas = aprox_dic - aprox_ene
    ea_deltas = ea_ene + ea_dic
    
    er_deltas = np.where(deltas != 0, (ea_deltas / np.abs(deltas)) * 100, np.inf)
    
    resultados = np.column_stack((años, deltas, ea_deltas, er_deltas))
    resultados_ordenados = resultados[resultados[:, 3].argsort()] 

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    filas = [[int(f[0]), round(f[1], 2), round(f[2], 2), round(f[3], 2)] for f in resultados_ordenados]
    escribir_seccion_csv(ruta_csv, 'a', '--- A4: variacion enero-diciembre por anio (mas confiable primero) ---',
    ['anio', 'variacion_clp', 'error_absoluto', 'error_relativo_pct'], filas,)

def graficar_cancelacion_mensual(valores, etiquetas, directorio):
    val_aprox = v_redondear(valores, 2)
    deltas_mes = np.diff(val_aprox) 
    ea_mes = np.abs(valores - val_aprox)
    ea_propagado_mes = ea_mes[1:] + ea_mes[:-1] 
    
    plt.figure(figsize=(10, 4))
    plt.bar(etiquetas[1:], deltas_mes, yerr=ea_propagado_mes)
    plt.axhline(0, color='black')
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Variacion Mes a Mes")
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/2_cancelacion_mensual.png'))
    plt.close()

if __name__ == '__main__':
    directorio_actual = os.path.dirname(__file__)
    ruta_csv = os.path.join(directorio_actual, '../data/dolar_observado_sii_2022_2025.csv')
    
    valores, etiquetas = cargar_csv(ruta_csv)
    
    analizar_cancelacion_a3(valores, directorio_actual)
    analizar_variacion_anual_a4(valores, directorio_actual)
    graficar_cancelacion_mensual(valores, etiquetas, directorio_actual)