import copy
import math
import random

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2


class Connect4:
    """Modelo minimo del tablero de Connect Four."""

    def __init__(self):
        # Matriz de 6x7 inicializada en vacio.
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def clone(self):
        # Clon profundo para simular jugadas sin tocar el tablero original.
        new_game = Connect4()
        new_game.board = copy.deepcopy(self.board)
        return new_game

    def actions(self):
        # Una columna es valida si su celda superior esta vacia.
        valid_moves = []
        for col in range(COLS):
            if self.board[0][col] == EMPTY:
                valid_moves.append(col)
        return valid_moves

    def drop_piece(self, col, piece):
        # Rechaza columnas fuera de rango o llenas.
        if col < 0 or col >= COLS or self.board[0][col] != EMPTY:
            return False

        # La ficha cae a la fila mas baja disponible de la columna.
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = piece
                return True
        return False

    def is_full(self):
        # Si no hay acciones posibles, el tablero esta lleno.
        return len(self.actions()) == 0

    def check_winner(self, piece):
        # 4 en linea horizontal.
        for row in range(ROWS):
            for col in range(COLS - 3):
                if (self.board[row][col] == piece and
                    self.board[row][col + 1] == piece and
                    self.board[row][col + 2] == piece and
                    self.board[row][col + 3] == piece):
                    return True

        # 4 en linea vertical.
        for row in range(ROWS - 3):
            for col in range(COLS):
                if (self.board[row][col] == piece and
                    self.board[row + 1][col] == piece and
                    self.board[row + 2][col] == piece and
                    self.board[row + 3][col] == piece):
                    return True

        # Diagonal descendente (\\).
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if (self.board[row][col] == piece and
                    self.board[row + 1][col + 1] == piece and
                    self.board[row + 2][col + 2] == piece and
                    self.board[row + 3][col + 3] == piece):
                    return True

        # Diagonal ascendente (/).
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if (self.board[row][col] == piece and
                    self.board[row - 1][col + 1] == piece and
                    self.board[row - 2][col + 2] == piece and
                    self.board[row - 3][col + 3] == piece):
                    return True
        return False

    def is_terminal(self):
        # Terminal: alguien gano o no quedan movimientos.
        return self.check_winner(PLAYER) or self.check_winner(AI) or self.is_full()


minimax_nodes_visited = 0
alpha_beta_nodes_visited = 0


def evaluate_window(window, piece):
    """Evalua una ventana de 4 casillas para la heuristica."""
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4

    # Penaliza dejar amenazas directas del rival.
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 12

    return score


def score_position(board, piece):
    """Heuristica total del tablero."""
    score = 0
    grid = board.board

    # Jugar al centro suele abrir mas lineas de victoria.
    center_col = COLS // 2
    center_array = [grid[r][center_col] for r in range(ROWS)]
    score += center_array.count(piece) * 3

    # Horizontal
    for r in range(ROWS):
        row_array = grid[r]
        for c in range(COLS - 3):
            score += evaluate_window(row_array[c:c + 4], piece)

    # Vertical
    for c in range(COLS):
        col_array = [grid[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            score += evaluate_window(col_array[r:r + 4], piece)

    # Diagonal descendente
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [grid[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Diagonal ascendente
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [grid[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def ordered_actions(board):
    """Ordena jugadas desde el centro para mejorar la poda."""
    center = COLS // 2
    return sorted(board.actions(), key=lambda col: abs(col - center))


def minimax_pure(board, depth, maximizing_player):
    """Minimax recursivo sin poda (Task 2.1)."""
    global minimax_nodes_visited
    minimax_nodes_visited += 1

    valid_locations = board.actions()
    is_term = board.is_terminal()

    if depth == 0 or is_term:
        if is_term:
            if board.check_winner(AI):
                return 1000000000
            if board.check_winner(PLAYER):
                return -1000000000
            return 0
        return score_position(board, AI)

    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            b_copy = board.clone()
            b_copy.drop_piece(col, AI)
            value = max(value, minimax_pure(b_copy, depth - 1, False))
        return value

    value = math.inf
    for col in valid_locations:
        b_copy = board.clone()
        b_copy.drop_piece(col, PLAYER)
        value = min(value, minimax_pure(b_copy, depth - 1, True))
    return value


def get_best_move_minimax(board, depth=4):
    """Mejor jugada de la IA usando Minimax puro (profundidad 3 o 4)."""
    global minimax_nodes_visited
    minimax_nodes_visited = 0

    valid_locations = board.actions()
    if not valid_locations:
        return None

    best_score = -math.inf
    best_col = valid_locations[0]

    for col in valid_locations:
        b_copy = board.clone()
        b_copy.drop_piece(col, AI)
        score = minimax_pure(b_copy, depth - 1, False)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def get_best_move(board, depth):
    """Alias solicitado en Task 2.1."""
    return get_best_move_minimax(board, depth)


def alpha_beta(board, depth, alpha, beta, maximizing_player):
    """Busqueda Minimax con poda Alfa-Beta."""
    global alpha_beta_nodes_visited
    alpha_beta_nodes_visited += 1

    valid_locations = board.actions()
    is_term = board.is_terminal()

    if depth == 0 or is_term:
        if is_term:
            if board.check_winner(AI):
                return 1000000000
            if board.check_winner(PLAYER):
                return -1000000000
            return 0
        return score_position(board, AI)

    valid_locations = ordered_actions(board)

    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            b_copy = board.clone()
            b_copy.drop_piece(col, AI)
            value = max(value, alpha_beta(b_copy, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    value = math.inf
    for col in valid_locations:
        b_copy = board.clone()
        b_copy.drop_piece(col, PLAYER)
        value = min(value, alpha_beta(b_copy, depth - 1, alpha, beta, True))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def get_best_move_alpha_beta(board, depth=5):
    """Mejor jugada de la IA usando Alfa-Beta."""
    global alpha_beta_nodes_visited
    alpha_beta_nodes_visited = 0

    valid_locations = ordered_actions(board)
    if not valid_locations:
        return None

    best_score = -math.inf
    best_col = valid_locations[0]
    alpha = -math.inf
    beta = math.inf

    for col in valid_locations:
        b_copy = board.clone()
        b_copy.drop_piece(col, AI)
        score = alpha_beta(b_copy, depth - 1, alpha, beta, False)

        if score > best_score:
            best_score = score
            best_col = col

        alpha = max(alpha, best_score)

    return best_col


def compare_minimax_vs_alpha_beta(board, depth=4):
    """Compara Minimax puro vs Alfa-Beta en el mismo estado (Task 2.2)."""
    best_minimax = get_best_move_minimax(board, depth)
    nodes_minimax = minimax_nodes_visited

    best_ab = get_best_move_alpha_beta(board, depth)
    nodes_ab = alpha_beta_nodes_visited

    print(f"Comparacion en profundidad {depth}")
    print(f"Minimax puro -> mejor columna: {best_minimax}, nodos: {nodes_minimax}")
    print(f"Alfa-Beta    -> mejor columna: {best_ab}, nodos: {nodes_ab}")

    if nodes_minimax > 0:
        reduction = (1 - (nodes_ab / nodes_minimax)) * 100
        print(f"Reduccion de nodos con Alfa-Beta: {reduction:.2f}%")


def play_alpha_beta_vs_random(depth=5, verbose=True):
    """Partida simple: IA (Alfa-Beta) contra agente aleatorio."""
    game = Connect4()
    turn = AI

    if verbose:
        print("Inicio: IA (Alfa-Beta) vs Aleatorio")

    while not game.is_terminal():
        if turn == AI:
            col = get_best_move_alpha_beta(game, depth)
            label = "IA"
        else:
            col = random.choice(game.actions())
            label = "Aleatorio"

        game.drop_piece(col, turn)
        if verbose:
            print(f"{label} juega columna {col}")

        turn = PLAYER if turn == AI else AI

    if game.check_winner(AI):
        print("Resultado: Gana IA (Alfa-Beta)")
        return AI
    if game.check_winner(PLAYER):
        print("Resultado: Gana Aleatorio")
        return PLAYER

    print("Resultado: Empate")
    return EMPTY


def benchmark_alpha_beta_vs_random(num_games=20, depth=5):
    """Corre varias partidas para medir rendimiento vs aleatorio."""
    wins = 0
    losses = 0
    draws = 0

    for _ in range(num_games):
        game = Connect4()
        turn = AI

        while not game.is_terminal():
            if turn == AI:
                col = get_best_move_alpha_beta(game, depth)
            else:
                col = random.choice(game.actions())

            game.drop_piece(col, turn)
            turn = PLAYER if turn == AI else AI

        if game.check_winner(AI):
            wins += 1
        elif game.check_winner(PLAYER):
            losses += 1
        else:
            draws += 1

    print(f"Benchmark IA vs Aleatorio | partidas={num_games}, profundidad={depth}")
    print(f"IA gana: {wins} | IA pierde: {losses} | Empates: {draws}")
    print(f"Win rate IA: {wins / num_games:.2%}")


def play_human_vs_alpha_beta(depth=5, human_piece=PLAYER):
    """Modo interactivo para jugar contra la IA en consola."""
    game = Connect4()
    ai_piece = AI if human_piece == PLAYER else PLAYER
    turn = PLAYER

    print("Tu vs IA (Alfa-Beta)")
    print(f"Tu ficha: {human_piece} | IA ficha: {ai_piece}")

    while not game.is_terminal():
        if turn == human_piece:
            valid = game.actions()
            col_text = input(f"Tu turno. Elige columna {valid}: ")
            try:
                col = int(col_text)
            except ValueError:
                print("Entrada invalida. Escribe un numero de columna.")
                continue

            if col not in valid:
                print("Columna no valida. Intenta otra vez.")
                continue

            game.drop_piece(col, human_piece)
            print(f"Tu juegas columna {col}")
        else:
            col = get_best_move_alpha_beta(game, depth)
            game.drop_piece(col, ai_piece)
            print(f"IA juega columna {col}")

        turn = ai_piece if turn == human_piece else human_piece

    if game.check_winner(human_piece):
        print("Resultado final: Ganaste")
    elif game.check_winner(ai_piece):
        print("Resultado final: Gana la IA")
    else:
        print("Resultado final: Empate")


def test():
    game = Connect4()
    game.drop_piece(3, PLAYER)
    game.drop_piece(3, AI)
    game.drop_piece(2, PLAYER)
    game.drop_piece(4, AI)

    # Task 2.2: mismo estado y misma profundidad para comparar nodos.
    compare_minimax_vs_alpha_beta(game, depth=4)

    col = get_best_move_alpha_beta(game, 5)
    print(f"Mejor columna con Alfa-Beta (Profundidad 5): {col}")
    print(f"Nodos visitados con Alfa-Beta (d=5): {alpha_beta_nodes_visited}")

    benchmark_alpha_beta_vs_random(num_games=20, depth=5)


if __name__ == '__main__':
    test()
