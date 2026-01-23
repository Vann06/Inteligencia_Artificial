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
    salarios = np.random.randint(3000, 25000, size=n)

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


def main() -> None:
    """
    Orquesta el flujo:
    1) Generar dataset sucio
    2) Imputar faltantes manualmente
    3) Undersampling manual para balancear clases
    """
    # 1) Generar dataset sucio
    df_sucio = genera_data_sucia()
    print("Dataset Sucio:")
    print("Filas, Columnas:", df_sucio.shape)
    print("NaN en Edad:", df_sucio["Edad"].isna().sum())
    print("Distribución Compro_Producto:\n", df_sucio["Compro_Producto"].value_counts())
    print("\n Muestra del dataset sucio:\n", df_sucio.head())

    print(":D")


if __name__ == "__main__":
    main()
