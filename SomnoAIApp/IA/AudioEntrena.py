import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Función para extraer características de audio (MFCC, amplitud, duración, frecuencia dominante)
def extraer_caracteristicas(ruta_audio):
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
    
    return np.hstack([mfcc_mean, duracion, amplitud_promedio, frec_dominante])

# Función para procesar todos los audios de una carpeta
def procesar_carpetas(ruta_carpeta, etiqueta):
    X = []
    y = []
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(".wav"):
            ruta_audio = os.path.join(ruta_carpeta, archivo)
            caracteristicas = extraer_caracteristicas(ruta_audio)
            X.append(caracteristicas)  # Agregar las características extraídas
            y.append(etiqueta)  # Etiqueta 1 para apnea, 0 para sano
    return X, y

# Procesar los audios de ronquidos sanos y apneicos
X_sanos, y_sanos = procesar_carpetas('/content/ronquidos_sanos/', etiqueta=0)
X_apnea, y_apnea = procesar_carpetas('/content/ronquidos_apnea/', etiqueta=1)

# Unir los datos de ambas carpetas
X = X_sanos + X_apnea
y = y_sanos + y_apnea

# Convertir a arrays de numpy
X = np.array(X)
y = np.array(y)

# Dividir los datos en conjunto de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Guardar el modelo entrenado como .pkl
joblib.dump(modelo, 'predecirAudio.pkl')

print("Modelo entrenado y guardado como 'predecirAudio.pkl'")