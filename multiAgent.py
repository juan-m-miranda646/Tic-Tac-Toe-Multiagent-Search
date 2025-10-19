# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 10:48:02 2025
@author: warre
prints the principal path and also writes it to a text file each time you run the algorithm
"""
from GameStatus_5120 import GameStatus

# Global path tracker
path_trace = []


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool,
            alpha=float('-inf'), beta=float('inf'), indent: str = ""):
    global path_trace

    terminal = game_state.is_terminal()
    if (depth == 0) or terminal:
        score = game_state.get_scores(terminal)
        return score, None

    best_move = None

    # --- MAX player (X) ---
    if maximizingPlayer:
        maxEval = float('-inf')
        for move in game_state.get_moves():
            child = game_state.get_new_state(move)
            eval_score, _ = minimax(child, depth - 1, False, alpha, beta, indent + "   ")
            if eval_score > maxEval:
                maxEval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        #path_trace.append((depth, 'MAX' if maximizingPlayer else 'MIN', best_move, maxEval if maximizingPlayer else minEval))
        return maxEval, best_move

    # --- MIN player (O) ---
    else:
        minEval = float('inf')
        for move in game_state.get_moves():
            child = game_state.get_new_state(move)
            eval_score, _ = minimax(child, depth - 1, True, alpha, beta, indent + "   ")
            if eval_score < minEval:
                minEval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        path_trace.append((depth, 'MIN', best_move, minEval))
        return minEval, best_move

def negamax(game_state: GameStatus, depth: int, alpha=float('-inf'), beta=float('inf'),
            color=1, indent=""):
    """
    Negamax search with alpha-beta pruning.
    color = +1 for X (maximizing), -1 for O (minimizing)
    Returns: (score, best_move)
    """
    terminal = game_state.is_terminal()
    if depth == 0 or terminal:
        score = color * game_state.get_scores(terminal)
        print(f"{indent}↳ [BASE] Depth={depth}, Color={color}, Winner={game_state.winner}, Score={score}")
        return score, None

    max_score = float('-inf')
    best_move = None

    for move in game_state.get_moves():
        child = game_state.get_new_state(move)
        eval_score, _ = negamax(child, depth - 1, -beta, -alpha, -color, indent + "   ")
        eval_score = -eval_score  # flip sign for the current player

        print(f"{indent}Move {move} at depth={depth}, eval={eval_score}, α={alpha}, β={beta}")

        if eval_score > max_score:
            max_score = eval_score
            best_move = move

        alpha = max(alpha, eval_score)
        if alpha >= beta:
            print(f"{indent}PRUNE at depth={depth} on move {move} (α={alpha}, β={beta})")
            break

    print(f"{indent}✔ RETURN NEGAMAX depth={depth} → best_move={best_move}, score={max_score}")
    return max_score, best_move

def print_principal_path():
    """Prints the condensed path of chosen moves."""
    print("\n🔍 Principal Path (Best Move Sequence):")
    for level in sorted(path_trace, key=lambda x: x[0], reverse=True):
        d, player, move, val = level
        print(f"Depth {d:<2} | {player:<3} chose move {move} with score {val}")
    if path_trace:
        print("----------------------------------------------------")
        print(f"Final Evaluation: {path_trace[0][3]}  (from root depth {path_trace[0][0]})")


def write_principal_path_to_file(filename="principal_path_log.txt"):
    """Writes the principal path (chosen moves) to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Principal Path (Best Move Sequence)\n")
        f.write("====================================\n")
        for level in sorted(path_trace, key=lambda x: x[0], reverse=True):
            d, player, move, val = level
            f.write(f"Depth {d:<2} | {player:<3} chose move {move} with score {val}\n")
        if path_trace:
            f.write("------------------------------------\n")
            f.write(f"Final Evaluation: {path_trace[0][3]} (from root depth {path_trace[0][0]})\n")
    print(f"\n🗂 Principal path has been saved to: {filename}")