import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# Al no existir restricciones al momento de preparar los datos, se optó por usar la librería sklearn para que los datos fueran 100% fiables para los demás ejercicios.

# --- PASO 1: Carga y Limpieza ---
df = pd.read_csv('dataset_phishing.csv')

if 'url' in df.columns:
    df = df.drop(columns=['url'])

# --- PASO 2: Codificación ---
le = LabelEncoder()
df['status'] = le.fit_transform(df['status'])
print(f"Clases codificadas: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# --- PASO 3: Selección de Features ---
correlations = df.corr()['status'].abs().sort_values(ascending=False)
top_2_features = correlations.index[1:3].tolist()
print(f"Features seleccionadas: {top_2_features}")

X = df[top_2_features].values
y = df['status'].values

# --- PASO 4: Escalado ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- PASO 5: Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"Dimensiones de entrenamiento: {X_train.shape}")
print(f"Dimensiones de prueba: {X_test.shape}")