import pandas as pd
import numpy as np

# Función para generar datos aleatorios y crear el archivo de entrenamiento
def generar_datos_entrenamiento(num_filas=1000):
    np.random.seed(42)  # Fijar la semilla para reproducibilidad
    
    # Generar datos aleatorios
    frecuencia_cardiaca = np.random.randint(50, 120, size=num_filas)  # Frecuencia cardíaca (50 a 120 latidos por minuto)
    saturacion_oxigeno = np.random.uniform(85, 100, size=num_filas)  # Saturación de oxígeno (85% a 100%)
    movimientos = np.random.randint(0, 2, size=num_filas)  # Movimientos (0 = no, 1 = sí)
    respiracion = np.random.randint(10, 25, size=num_filas)  # Respiraciones por minuto (10 a 25)
    
    # Generar etiqueta de apnea (1 = apnea, 0 = no apnea) basada en una combinación aleatoria de los valores anteriores
    apnea = np.where(
        (frecuencia_cardiaca < 60) & (saturacion_oxigeno < 90) & (respiracion < 15),  # Condiciones indicativas de apnea
        1,  # Apnea
        0  # No apnea
    )
    
    # Crear un DataFrame
    df = pd.DataFrame({
        'frecuencia_cardiaca': frecuencia_cardiaca,
        'saturacion_oxigeno': saturacion_oxigeno,
        'movimientos': movimientos,
        'respiracion': respiracion,
        'apnea': apnea
    })
    
    # Guardar como CSV
    df.to_csv('entrenamiento_apnea.csv', index=False)
    print("Archivo de entrenamiento generado: entrenamiento_apnea.csv")

# Generar el CSV de entrenamiento
generar_datos_entrenamiento()