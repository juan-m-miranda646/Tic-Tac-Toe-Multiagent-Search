# -*- coding: utf-8 -*-
import numpy as np
import copy

class GameStatus:
    def __init__(self, board_state=None, turn_O=False):
        # Initialize board to 3x3 if not given
        if board_state is None:
            self.board_state = np.zeros((3, 3), dtype=int)
        else:
            self.board_state = np.array(board_state, dtype=int)

        self.turn_O = turn_O  # True = O’s turn (minimizer), False = X’s turn (maximizer)
        self.winner = None
        
        # validation for grid size (3x3, 4x4, 5x5)
        if self.board_state.ndim != 2 or self.board_state.shape[0] != self.board_state.shape[1]:
            raise ValueError("Board must be a 3x3, 4x4, or 5x5 matrix.")
        # ensures that the board is square and the size is that of 3x3, 4x4, or 5x5
        n = int(self.board_state.shape[0])
        if n not in (3, 4, 5):
            raise ValueError("Board must be a 3X3, 4x4, or 5x5 matrix.")

        # cache (item stored) to remember the size of the board
        self._n = n

    # -------------------------------------------------------------------------
    def is_terminal(self):
        """
        Checks whether the game has reached a terminal state:
        - Win for X (1)
        - Win for O (-1)
        - Draw (no empty cells)
        Returns True if terminal, False otherwise.
        """
        
        # variable for size of board stored in cache
        n = getattr(self, "_n", self.board_state.shape[0])
        b = self.board_state
        
        # Check rows and columns
        for i in range(n):
            row_sum = int(np.sum(b[i, :]))
            if abs(row_sum) == n:
                self.winner = 1 if row_sum == n else -1
                return True

            col_sum = int(np.sum(b[:, i]))
            if abs(col_sum) == n:
                self.winner = 1 if col_sum == n else -1
                return True

        # Check diagonals
        diag1 = int(np.sum([b[i, i] for i in range(n)]))
        diag2 = int(np.sum([b[i, n - 1 - i] for i in range(n)]))
        if abs(diag1) == n or abs(diag2) == n:
            self.winner = 1 if (diag1 == n or diag2 == n) else -1
            return True

        # Check for draw (no zeros)
        if not (0 in b):
            self.winner = 0
            return True

        return False

    # -------------------------------------------------------------------------
    def get_scores(self, _=None):
        """
        Returns a score based on the current game state:
        +1  if X (maximizer) wins
        -1  if O (minimizer) wins
         0  if draw or game not yet over
        """
        if self.winner == 1:
            return 1
        elif self.winner == -1:
            return -1
        else:
            return 0

    # -------------------------------------------------------------------------
    def get_negamax_scores(self, terminal):
        """
        Similar to get_scores(), but can assign larger magnitude values
        if desired for Negamax evaluation.
        """
        if self.winner == 1:
            return 100
        elif self.winner == -1:
            return -100
        else:
            return 0

    # -------------------------------------------------------------------------
    def get_moves(self):
        """
        Returns a list of all possible moves (empty cells) in (row, col) form.
        """
        moves = []
        n = self._n
        for r in range(n):
            for c in range(n):
                if self.board_state[r, c] == 0:
                    moves.append((r, c))
        return moves

    # -------------------------------------------------------------------------
    def get_new_state(self, move):
        """
        Returns a new GameStatus object after applying the given move.
        X = +1, O = -1.
        """
        new_board = copy.deepcopy(self.board_state)
        x, y = move
        new_board[x, y] = -1 if self.turn_O else 1
        return GameStatus(new_board, not self.turn_O)

    # -------------------------------------------------------------------------
    def __repr__(self):
        return str(self.board_state)