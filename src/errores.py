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

def analizar_error_representacion(valores, etiquetas, directorio):
    val_aprox = v_redondear(valores, 2)
    ea = np.abs(valores - val_aprox)
    er = (ea / valores) * 100

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    filas = zip(etiquetas, valores, val_aprox, np.round(ea, 4), np.round(er, 4))
    escribir_seccion_csv(ruta_csv, 'w','--- A1: error de representacion por mes (2 cifras significativas) ---',
        ['mes', 'precio_real', 'precio_aprox', 'error_absoluto', 'error_relativo_pct'],filas,)
    
    # Grafico 1
    plt.figure(figsize=(10, 4))
    plt.plot(etiquetas, valores, label='Real')
    plt.plot(etiquetas, val_aprox, label='Aprox')
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Dolar Real vs Aprox")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/1_serie_mensual.png'))
    plt.close()
    
    # Grafico 3
    plt.figure(figsize=(10, 4))
    plt.bar(etiquetas, ea)
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Error Absoluto de Representacion")
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/3_error_representacion.png'))
    plt.close()

def evaluar_compra_venta(precio_compra_real, precio_venta_real, monto=1000000):
    p_compra_aprox = v_redondear(precio_compra_real, 2)
    p_venta_aprox = v_redondear(precio_venta_real, 2)

    er_compra = np.abs(precio_compra_real - p_compra_aprox) / precio_compra_real * 100
    er_venta = np.abs(precio_venta_real - p_venta_aprox) / precio_venta_real * 100

    usd = monto / p_compra_aprox
    pesos_final = usd * p_venta_aprox
    ganancia = pesos_final - monto

    er_pesos_final = er_compra + er_venta
    ea_ganancia = (er_pesos_final / 100) * pesos_final

    rentabilidad = (ganancia / monto) * 100
    error_rentabilidad = (ea_ganancia / monto) * 100

    return {'p_compra_aprox': p_compra_aprox, 'p_venta_aprox': p_venta_aprox,'usd': usd, 'ganancia': ganancia, 'ea_ganancia': ea_ganancia,
    'rentabilidad': rentabilidad, 'error_rentabilidad': error_rentabilidad,}