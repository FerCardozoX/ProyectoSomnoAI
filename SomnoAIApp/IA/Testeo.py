import pandas as pd
import joblib
import numpy as np

def procesar_oxigeno_saturacion(archivo_csv):
    try:
        heart_rate_values = []

        with open(archivo_csv, 'r') as file:
            next(file)  # Saltar la primera línea (cabecera irrelevante)
            for index, line in enumerate(file, start=2):
                values = line.strip().split(',')
                if len(values) > 20:  # Verificar que haya suficientes columnas
                    heart_rate_value = values[20]  # Índice 20 para heart_rate

                    if heart_rate_value.strip():
                        try:
                            heart_rate_value = float(heart_rate_value)
                            heart_rate_values.append(heart_rate_value)
                        except ValueError:
                            pass

        if heart_rate_values:
            promedio_oxigeno = sum(heart_rate_values) / len(heart_rate_values)
            print(f"\nPromedio de com.samsung.health.oxygen_saturation.heart_rate: {promedio_oxigeno}")
            return promedio_oxigeno
        else:
            print("\nNo se encontraron valores válidos para calcular el promedio.")
            return 0  # Valor por defecto si no se encuentran valores válidos

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return 0

def procesar_heart_rate(archivo_csv):
    try:
        heart_rate_values = []

        with open(archivo_csv, 'r') as file:
            next(file)  # Saltar la primera línea (cabecera irrelevante)
            headers = next(file).strip().split(',')
            heart_rate_index = headers.index('com.samsung.health.heart_rate.heart_rate')

            for index, line in enumerate(file, start=3):
                values = line.strip().split(',')
                if len(values) > heart_rate_index:
                    heart_rate_value = values[heart_rate_index]

                    if heart_rate_value.strip():
                        try:
                            heart_rate_value = float(heart_rate_value)
                            heart_rate_values.append(heart_rate_value)
                        except ValueError:
                            pass

        if heart_rate_values:
            promedio_heart_rate = sum(heart_rate_values) / len(heart_rate_values)
            print(f"\nPromedio de com.samsung.health.heart_rate.heart_rate: {promedio_heart_rate}")
            return promedio_heart_rate
        else:
            print("\nNo se encontraron valores válidos para calcular el promedio.")
            return 0

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return 0

def procesar_breathing(archivo_csv):
    try:
        cycle_values = []

        with open(archivo_csv, 'r') as file:
            next(file)  # Saltar la primera línea (cabecera irrelevante)
            headers = next(file).strip().split(',')
            cycle_index = headers.index('cycle')

            for index, line in enumerate(file, start=3):
                values = line.strip().split(',')
                if len(values) > cycle_index:
                    cycle_value = values[cycle_index]

                    if cycle_value.strip():
                        try:
                            cycle_value = float(cycle_value)
                            cycle_values.append(cycle_value)
                        except ValueError:
                            pass

        if cycle_values:
            promedio_breathing = sum(cycle_values) / len(cycle_values)
            print(f"\nPromedio de cycle: {promedio_breathing} respiraciones por minuto")
            return promedio_breathing
        else:
            print("\nNo se encontraron valores válidos para calcular el promedio.")
            return 0

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return 0

# Función principal para ejecutar el procesamiento y la predicción
def main():
    # Procesar los archivos CSV
    promedio_oxigeno = procesar_oxigeno_saturacion('com.samsung.shealth.tracker.oxygen_saturation.20240426191109.csv')
    promedio_heart_rate = procesar_heart_rate('com.samsung.shealth.tracker.heart_rate.20240426191109.csv')
    promedio_breathing = procesar_breathing('com.samsung.shealth.breathing.20240426191109.csv')

    # Cargar el modelo entrenado
    modelo = joblib.load('cerebro_apnea.pkl')

    # Definir los parámetros utilizando los promedios calculados
    movimientos = 0  # Puedes ajustar este valor según tu lógica

    # Crear un array con los parámetros de entrada
    parametros_personales = np.array([[promedio_heart_rate, promedio_oxigeno, movimientos, promedio_breathing]])

    # Usar el modelo para predecir si hay apnea o no
    prediccion = modelo.predict(parametros_personales)

    # Mostrar el resultado
    if prediccion[0] == 1:
        print("Apnea detectada.")
    else:
        print("No hay apnea.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()