# Connect Four - Tasks 2


## Estructura del proyecto
- Notebook principal: Connect_Four.ipynb
- Script alternativo para pruebas por consola: test_minimax.py

## Task 2.1 - Logica base + Minimax puro

Requisitos:
- Clase Connect4 con estado del tablero.
- Movimientos validos con actions().
- Deteccion de estado terminal con is_terminal().
- Agente Minimax recursivo con get_best_move(board, depth).
- Profundidad limitada a d=3 o d=4.

Estado en este proyecto:
- Connect4 implementada.
- Minimax puro implementado como minimax_pure y get_best_move_minimax.
- Alias solicitado implementado: get_best_move(board, depth).
- Restriccion de profundidad para Minimax puro: usar depth=3 o depth=4.

Que mostrar en la presentacion:
1. Ejecutar definiciones de tablero y funciones.
2. Ejecutar una llamada a get_best_move_minimax(game, depth=4).
3. Explicar que Minimax puro explora muchos nodos.

## Task 2.2 - Poda Alfa-Beta + comparacion de nodos

Requisitos:
- Version recursiva que use alpha y beta.
- Demostrar en el mismo estado del tablero que Alfa-Beta visita menos nodos que Minimax puro.

Estado en este proyecto:
- Alfa-Beta implementado como alpha_beta y get_best_move_alpha_beta.
- Comparacion implementada como compare_minimax_vs_alpha_beta(board, depth=4).


## Task 2.3 - Heuristica 

Requisitos:
- Funcion evaluate(board) no aleatoria.
- Heuristica estrategica (centro, amenazas de 3+espacio, etc.).
  1) Alfa-Beta profundidad 5 o 6 vs agente aleatorio.
  2) Alfa-Beta profundidad 5 o 6 vs humano (tu o un companero).

Estado en este proyecto:
- Heuristica implementada con score_position y evaluate_window.
- Prioriza centro y ventanas de 4.
- Penaliza amenazas del rival.
- Partida vs aleatorio: play_alpha_beta_vs_random y benchmark_alpha_beta_vs_random.
- Partida vs humano: play_human_vs_alpha_beta.

## Estrategia heuristica implementada

La IA usa una heuristica de ataque + defensa:

- Evalua ventanas de 4 casillas (horizontal, vertical y diagonales).
- Suma puntos si la IA tiene:
  - 4 en linea: +100
  - 3 fichas + 1 vacia: +10
  - 2 fichas + 2 vacias: +4
- Resta puntos si el rival tiene 3 fichas + 1 vacia: -12 (bloqueo defensivo).
- Da bonus por controlar la columna central: +3 por cada ficha de IA en el centro.
- En estados terminales:
  - Gana IA: valor muy alto positivo.
  - Gana rival: valor muy alto negativo.
  - Empate: 0.

En resumen: prioriza centro, crear amenazas propias y bloquear amenazas inmediatas del oponente.


En Connect_Four.ipynb:
1. Ejecutar celdas de imports y clase Connect4.
2. Ejecutar celda del agente Alfa-Beta y heuristica.
3. Ejecutar celda de Task 2.2 (comparacion de nodos).
4. Ejecutar celda final de demo:
   - compare_minimax_vs_alpha_beta(game, depth=4)
   - benchmark_alpha_beta_vs_random(num_games=20, depth=5)
   - play_alpha_beta_vs_random(depth=5, verbose=True)
5. Ejecutar partida humana:
   - play_human_vs_alpha_beta(depth=5, human_piece=PLAYER)

## Guion corto sugerido para el video

1. "Implemente Connect4, Minimax puro y luego Alfa-Beta."
2. "Para Task 2.2, en el mismo estado y misma profundidad, Alfa-Beta visita menos nodos."
3. "Mi heuristica puntua control del centro, amenazas propias y bloqueos defensivos."
4. "Ahora muestro Alfa-Beta profundidad 5 contra un agente aleatorio."
5. "Finalmente juego yo contra la IA para intentar ganarle."


