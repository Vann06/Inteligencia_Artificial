import numpy as np

#Def que calcuila la regresion RMSE
def regresion_rsme(reals: list, predict: list):
    mse = np.square(np.subtract(reals, predict)).mean()
    rmse = np.sqrt(mse)
    return rmse

#Def que calcuila la regresion MAE
def regresion_mae(reals: list, predict: list):
    mae = np.absolute(np.subtract(reals, predict)).mean()
    return mae


def main():
    reales = [100, 150, 200, 250, 300]
    predichos = [110, 140, 210, 240, 500]

    rmse_result = regresion_rsme(reales, predichos)
    mae_result = regresion_mae(reales, predichos)

    print("RMSE:", rmse_result)
    print("MAE:", mae_result)

    print("El sistema de regresion que mas penalizo el ultimo resultado", predichos[-1], "fue la regresion RMSE\n")
    print("Esto es debido a que RMSE se comporta de manera exponencial lo que la hace penalizar mas errores a diferencia de MAE, que se comporta lineal\n")
    print("En un contexto de medicina, es importante fijarse en los errores, RMSE seria el modelo mas factible a utilizar\n")
    print("Si hablamos de dosis de medicamentos si solo hubo un error con un paciente y este error es grande MAE no lo registrara como tal, es lo mismo 10 errores de 1 que 1 de 10\n")
    print("RMSE penaliza los errores grandes, lo que hace mas visible si un valor varia mucho de los valores reales, y en estos casos donde es vital por la salud de la gente, es el mejor modelo\n")


if __name__ == "__main__":
    main()