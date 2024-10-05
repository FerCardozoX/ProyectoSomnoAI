import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import joblib

# 1. Función para extraer características de audio (MFCC, amplitud, duración, frecuencia dominante)
def extraer_caracteristicas(ruta_audio):
    try:
        y, sr = librosa.load(ruta_audio, sr=None)
        
        # Características: MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)

        # Características adicionales
        duracion = librosa.get_duration(y=y, sr=sr)
        amplitud_promedio = np.mean(np.abs(y))
        S = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        frec_dominante = freqs[np.argmax(S, axis=0)].mean()
        
        # Espectrograma (para la visualización)
        espectrograma = librosa.amplitude_to_db(S, ref=np.max)

        # Devolver las características como un diccionario
        return {
            'mfcc': mfcc_mean,
            'duracion': duracion,
            'amplitud': amplitud_promedio,
            'frecuencia_dominante': frec_dominante,
            'espectrograma': espectrograma,
            'y': y,  # Guardamos el audio original para la visualización
            'sr': sr  # Frecuencia de muestreo para la visualización
        }

    except Exception as e:
        print(f"Error al procesar el archivo {ruta_audio}: {e}")
        return None

# 2. Función para predecir apnea y mostrar visualizaciones
def predecir_audio_y_visualizar(ruta_audio):
    try:
        ruta_modelo= os.path.join(os.path.dirname(__file__),'predecirAudio.pkl')
        # Cargar el modelo entrenado
        modelo = joblib.load(ruta_modelo)

        # Extraer características del audio
        caracteristicas = extraer_caracteristicas(ruta_audio)

        # Verificar si se pudieron extraer las características
        if caracteristicas is None:
            return

        # Crear un vector con las características relevantes
        caracteristicas_vector = np.hstack([caracteristicas['mfcc'], 
                                            caracteristicas['duracion'], 
                                            caracteristicas['amplitud'], 
                                            caracteristicas['frecuencia_dominante']])
        caracteristicas_vector = np.array([caracteristicas_vector])  # Convertir a 2D para el modelo

        # Hacer la predicción con el modelo
        prediccion = modelo.predict(caracteristicas_vector)
        resultado_apnea = "Apnea detectada" if prediccion[0] == 1 else "No hay apnea"

        # Mostrar detalles adicionales del análisis
        detalles = {
            "duracion": caracteristicas['duracion'],
            "amplitud": caracteristicas['amplitud'],
            "frecuencia_dominante": caracteristicas['frecuencia_dominante']
        }
        print(f'Resultado para el nuevo audio: {resultado_apnea}')
        print(f"Detalles adicionales:\nDuración: {detalles['duracion']} segundos\nAmplitud: {detalles['amplitud']}\nFrecuencia dominante: {detalles['frecuencia_dominante']} Hz")
        
        # Visualizar el espectrograma
        visualizar_espectrograma(caracteristicas)

        # Visualizar la forma de onda
        visualizar_forma_onda(caracteristicas)

    except Exception as e:
        print(f"Error al hacer la predicción: {e}")

# 3. Función para visualizar el espectrograma
def visualizar_espectrograma(caracteristicas):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(caracteristicas['espectrograma'], sr=caracteristicas['sr'], x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma')
    plt.tight_layout()
    plt.show()

# 4. Función para visualizar la forma de onda del audio
def visualizar_forma_onda(caracteristicas):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(caracteristicas['y'], sr=caracteristicas['sr'])
    plt.title('Forma de onda del audio')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.show()


def main():
    ruta_audio = os.path.join(os.path.dirname(__file__),'Prueba1-normal.wav') # Asegúrate de que este archivo exista
    predecir_audio_y_visualizar(ruta_audio)
    try:
        resultado, detalles = predecir_audio_y_visualizar(ruta_audio)

        return {
            "resultado_apnea": resultado,
            "duracion": detalles["duracion"],
            "amplitud": detalles["amplitud"],
            "frecuencia_dominante": detalles["frecuencia_dominante"],
            # Si quieres devolver el espectrograma en bruto para análisis futuro
            "espectrograma": detalles["espectrograma"]  
        }

    except Exception as e:
        print(f"Error en la función main: {e}")
        return None