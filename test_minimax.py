import copy
import math

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


def evaluate_basic(board):
    # Heuristica basica: solo premia/penaliza victorias directas.
    if board.check_winner(AI):
        return 1000
    elif board.check_winner(PLAYER):
        return -1000
    return 0


def minimax(board, depth, maximizingPlayer):
    """Devuelve el valor Minimax del estado actual."""
    global minimax_nodes_visited
    minimax_nodes_visited += 1

    # Caso base: profundidad agotada o estado terminal.
    is_term = board.is_terminal()
    if depth == 0 or is_term:
        if is_term:
            if board.check_winner(AI):
                return 100000000
            elif board.check_winner(PLAYER):
                return -100000000
            else:
                return 0
        else:
            return evaluate_basic(board)

    valid_locations = board.actions()
    if not valid_locations:
        return evaluate_basic(board)

    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            b_copy = board.clone()
            b_copy.drop_piece(col, AI)
            new_score = minimax(b_copy, depth - 1, False)
            if new_score is not None and new_score > value:
                value = new_score
        return value if value != -math.inf else 0
    else:
        value = math.inf
        for col in valid_locations:
            b_copy = board.clone()
            b_copy.drop_piece(col, PLAYER)
            new_score = minimax(b_copy, depth - 1, True)
            if new_score is not None and new_score < value:
                value = new_score
        return value if value != math.inf else 0


def get_best_move(board, depth):
    """Elige la mejor columna para la IA explorando hasta `depth`."""
    global minimax_nodes_visited
    minimax_nodes_visited = 0

    valid_locations = board.actions()
    best_score = -math.inf
    best_col = valid_locations[0] if valid_locations else None

    for col in valid_locations:
        b_copy = board.clone()
        b_copy.drop_piece(col, AI)
        score = minimax(b_copy, depth - 1, False)

        if score is not None and score > best_score:
            best_score = score
            best_col = col

    return best_col


def test():
    game = Connect4()
    # Posicion de ejemplo para probar la decision de la IA.
    game.drop_piece(3, PLAYER)
    game.drop_piece(3, AI)
    game.drop_piece(2, PLAYER)
    game.drop_piece(4, AI)

    col = get_best_move(game, 4)
    print(f"Mejor columna a jugar (Profundidad 4): {col}")
    print(f"Nodos visitados con Minimax Puro: {minimax_nodes_visited}")


if __name__ == '__main__':
    test()
