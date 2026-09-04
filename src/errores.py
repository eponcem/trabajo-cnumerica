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

def analizar_ejemplo_a2(valores, etiquetas, directorio, idx_compra=17, idx_venta=36):
    p_compra_real = valores[idx_compra]
    p_venta_real = valores[idx_venta]
    r = evaluar_compra_venta(p_compra_real, p_venta_real)
    er_ganancia_pct = abs(r['ea_ganancia'] / r['ganancia']) * 100 if r['ganancia'] != 0 else float('inf')

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv, 'a',
        '--- A2: compra-venta de ejemplo ---',
        ['mes_compra', 'mes_venta', 'ganancia_clp', 'error_absoluto_clp', 'error_relativo_pct'],
        [[etiquetas[idx_compra], etiquetas[idx_venta], round(r['ganancia'], 2),
          round(r['ea_ganancia'], 2), round(er_ganancia_pct, 2)]],
    )

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

def analizar_compra_venta(valores, etiquetas, directorio):
    monto = 1000000
    idx_min = np.argmin(valores)
    idx_max = np.argmax(valores)
    p_compra_real = valores[idx_min]

    er_compra = np.abs(p_compra_real - v_redondear(p_compra_real, 2)) / p_compra_real * 100

    meses_venta = valores[idx_min+1:]
    etiq_venta = etiquetas[idx_min+1:]
    p_venta_aprox = v_redondear(meses_venta, 2)

    er_venta = np.abs(meses_venta - p_venta_aprox) / meses_venta * 100

    usd = monto / v_redondear(p_compra_real, 2)
    pesos_final = usd * p_venta_aprox
    ganancia = pesos_final - monto

    er_pesos_final = er_compra + er_venta 
    ea_ganancia = (er_pesos_final / 100) * pesos_final 
    
    rentabilidad = (ganancia / monto) * 100
    error_rentabilidad = (ea_ganancia / monto) * 100
    
    # Grafico 4
    plt.figure(figsize=(10, 4))
    plt.errorbar(etiq_venta, rentabilidad, yerr=error_rentabilidad, fmt='o-')
    plt.axhline(0, color='black')
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Rentabilidad desde el Minimo")
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/4_rentabilidad.png'))
    plt.close()

    r_optimo = evaluar_compra_venta(valores[idx_min], valores[idx_max])
    conclusion_solida = bool(abs(r_optimo['ganancia']) > r_optimo['ea_ganancia'])

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')

    filas_tabla = zip(etiq_venta, np.round(meses_venta, 2), np.round(ganancia, 2),
                       np.round(ea_ganancia, 2), np.round(er_pesos_final, 2))
    escribir_seccion_csv(ruta_csv, 'a','--- A5 (detalle grafico 4): comprar en el minimo, vender en cada mes posterior ---',
    ['mes_venta', 'precio_venta_real', 'ganancia_clp', 'error_absoluto_clp', 'error_relativo_pct'],filas_tabla,)

    escribir_seccion_csv(ruta_csv, 'a','--- A5 (respuesta): comprar en el minimo, vender en el maximo del periodo ---',
    ['mes_compra', 'mes_venta', 'rentabilidad_pct', 'error_pct', 'conclusion_solida'],[[etiquetas[idx_min], etiquetas[idx_max], round(r_optimo['rentabilidad'], 2),
    round(r_optimo['error_rentabilidad'], 2), conclusion_solida]],)

if __name__ == '__main__':
    directorio_actual = os.path.dirname(__file__)
    ruta_csv_datos = os.path.join(directorio_actual, '../data/dolar_observado_sii_2022_2025.csv')
    valores, etiquetas = cargar_csv(ruta_csv_datos)
    
    analizar_error_representacion(valores, etiquetas, directorio_actual)
    analizar_ejemplo_a2(valores, etiquetas, directorio_actual)
    analizar_compra_venta(valores, etiquetas, directorio_actual)