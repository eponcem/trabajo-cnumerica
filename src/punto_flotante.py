import numpy as np
import os
import struct
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv
from errores import escribir_seccion_csv

def float_a_bits(valor):
    val_f32 = np.float32(valor)
    empaquetado = struct.pack('>f', val_f32)
    entero = struct.unpack('>I', empaquetado)[0]
    return f"{entero:032b}"

def analizar_representacion_flotante(valores, directorio):
    v_min = np.min(valores)
    v_max = np.max(valores)
    
    bits_min = float_a_bits(v_min)
    bits_max = float_a_bits(v_max)
    
    ulp_min = np.spacing(np.float32(v_min))
    ulp_max = np.spacing(np.float32(v_max))
    
    # Resta entre minimo y maximo para evaluar perdida de bits en mantisa
    f64_diff = np.float64(v_max) - np.float64(v_min)
    f32_diff = np.float32(v_max) - np.float32(v_min)
    error_resta = np.abs(f64_diff - np.float64(f32_diff))
    
    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(ruta_csv, 'a',
        '--- B1-B4: analisis de punto flotante ieee 754 (float32 vs float64) ---',
        ['parametro', 'valor_minimo', 'valor_maximo', 'diferencia_ulp_o_error'],
        [
            ['valor_real', round(v_min, 4), round(v_max, 4), '-'],
            ['bits_signo_exp_mantisa', bits_min, bits_max, '-'],
            ['ulp_float32', float(ulp_min), float(ulp_max), float(ulp_max - ulp_min)],
            ['resta_max_min', float(f32_diff), float(f64_diff), float(error_resta)]
        ])

def analizar_deriva(valores, etiquetas, directorio):
    monto = np.float32(1000000.0)
    v_f32 = np.float32(valores)
    
    usd = monto / v_f32
    recuperado = usd * v_f32
    deriva = monto - recuperado 
    
    plt.figure(figsize=(10, 4))
    plt.plot(etiquetas, deriva)
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Deriva en Float32")
    plt.ylabel("CLP")
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/5_deriva_flotante.png'))
    plt.close()

if __name__ == '__main__':
    directorio_actual = os.path.dirname(__file__)
    ruta_csv_datos = os.path.join(directorio_actual, '../data/dolar_observado_sii_2022_2025.csv')
    valores, etiquetas = cargar_csv(ruta_csv_datos)
    
    analizar_representacion_flotante(valores, directorio_actual)
    analizar_deriva(valores, etiquetas, directorio_actual)