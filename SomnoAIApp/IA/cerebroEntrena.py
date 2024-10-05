import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import joblib

# Cargar el archivo de entrenamiento generado
df = pd.read_csv('entrenamiento_apnea.csv')

# Seleccionar las características (X) y la etiqueta (y)
X = df[['frecuencia_cardiaca', 'saturacion_oxigeno', 'movimientos', 'respiracion']]
y = df['apnea']

# Dividir los datos en conjunto de entrenamiento y de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de red neuronal
modelo = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
modelo.fit(X_train, y_train)

# Guardar el modelo entrenado en un archivo
joblib.dump(modelo, 'cerebro_apnea.pkl')
print("Modelo entrenado y guardado como cerebro_apnea.pkl")