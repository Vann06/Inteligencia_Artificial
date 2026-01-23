"""
Task 2 - Ingeniería de Datos.
Genera un dataset sintético, imputa valores faltantes manualmente y balancea clases via undersampling.
"""
import numpy as np
import pandas as pd

"""
Generar el DataFrame con 100 filas y 3 columnas
Edad, Salario y Compro_Producto 0/1
"""
def genera_data_sucia(
        n: int = 100,
        majority_count = 90, #no compro producto 0 
        minority_count = 10, #si compro producto 
        missing_rate: float = 0.1, # valores NaN 10% en edad
        seed: int = 42
        
) -> pd.DataFrame:
    if majority_count + minority_count != n:
        raise ValueError("La suma de majority_count y minority_count debe ser igual a n.")
    np.random.seed(seed)
    # Generar Edades y Salarios
    edades = np.random.randint(18, 70, size=n).astype(float) 
    salarios = np.random.randint(3000, 25001, size=n)

    # Generar Compro_Producto con distribución desbalanceada
    compro_producto = np.array([0] * majority_count + [1] * minority_count )
    np.random.shuffle(compro_producto)

    # construir DataFrame
    df = pd.DataFrame({
        "Edad": edades,
        "Salario": salarios,
        "Compro_Producto": compro_producto
    })

    # Introducir valores NaN en Edad
    n_missing = int(missing_rate * n)
    missing_indices = np.random.choice(df.index, n_missing, replace=False)
    df.loc[missing_indices, "Edad"] = np.nan

    return df

# Manejo de Datos Faltantes 
def manejo_edad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputar valores faltantes en la columna 'Edad' con promedio de la columna.
    """
    promedio_edad = df["Edad"].mean()

    for i in df.index:
        if pd.isna(df.loc[i, "Edad"]):
            df.loc[i, "Edad"] = promedio_edad

    
    # El utilizar el promedio puede afectar si la distribución 
    # de edad es muy alta o valores atípicos. Si existiera alguien con 100 años por ejemplo 
    # Es más seguro utilizar la mediana en estos casos porque es más robusta 
    #a valores atípicos.

    return df

def undersampling(df: pd.DataFrame, target_column: str = "Compro_Producto", seed: int = 42) -> pd.DataFrame:
    """
    Realizar undersampling manual para balancear las clases en 'Compro_Producto'.
    """
    np.random.seed(seed)
    # Separar las clases
    df_min = df[df[target_column] == 1]
    df_maj = df[df[target_column] == 0]

    # elegir aleatorio las mayoria
    n_min = len(df_min)
    maj_sample_idx = np.random.choice(df_maj.index, n_min, replace=False)

    #construir df balanceado 
    df_maj_sample = df_maj.loc[maj_sample_idx]
    df_balanceado = pd.concat([df_min, df_maj_sample], axis = 0)
    df_balanceado = df_balanceado.sample(frac=1, random_state=seed).reset_index(drop=True)  # mezclar filas
    return df_balanceado

def main() -> None:
    """
    1) Generar dataset sucio
    2) Imputar faltantes manualmente
    3) Undersampling manual para balancear clases
    """
    df_sucio = genera_data_sucia()
    print("==== Generacion de Dataset Sucio ====")
    print("Filas, Columnas:", df_sucio.shape)
    print("NaN en Edad:", df_sucio["Edad"].isna().sum())
    print("Distribución Compro_Producto:\n", df_sucio["Compro_Producto"].value_counts())
    print("\n Muestra del dataset sucio:\n", df_sucio.head())

    print("==== Manejo de Datos Faltantes ====")
    df = manejo_edad(df_sucio)
    print("\n Dataset después de imputar Edad:")
    print("NaN en Edad:", df["Edad"].isna().sum())
    print(df.head())

    print("==== Manejo de Datos Desbalanceados ====")
    print("\nConteo antes de balancear:\n", df["Compro_Producto"].value_counts())
    df_balanceado = undersampling(df)
    print("\nConteo después de balancear:\n", df_balanceado["Compro_Producto"].value_counts())
    print("Tamaño df_balanceado:", df_balanceado.shape)
    print("\n Muestra del dataset balanceado:\n", df_balanceado.head())
    print("fin :D")


if __name__ == "__main__":
    main()
