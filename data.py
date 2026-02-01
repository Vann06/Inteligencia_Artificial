import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# --- PASO 1: Carga y Limpieza ---
df = pd.read_csv('dataset_phishing.csv')

# Eliminamos la columna 'url' (ID único irrelevante para el modelo)
if 'url' in df.columns:
    df = df.drop(columns=['url'])

# --- PASO 2: Codificación ---
# Convertimos 'legitimate'/'phishing' a 0 y 1
le = LabelEncoder()
df['status'] = le.fit_transform(df['status'])
print(f"Clases codificadas: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# --- PASO 3: Selección de Features ---
# Buscamos las 2 variables con mayor correlación absoluta
correlations = df.corr()['status'].abs().sort_values(ascending=False)
top_2_features = correlations.index[1:3].tolist() # [1:3] porque el 0 es 'status'
print(f"Features seleccionadas: {top_2_features}")

# Creamos nuestros sets de datos finales
X = df[top_2_features].values # .values para tener numpy arrays puros
y = df['status'].values

# --- PASO 4: Escalado (OBLIGATORIO) ---
# Estandarizamos para que la media sea 0 y la desviación 1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- PASO 5: Split ---
# 80% Entrenamiento, 20% Test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"Dimensiones de entrenamiento: {X_train.shape}")
print(f"Dimensiones de prueba: {X_test.shape}")