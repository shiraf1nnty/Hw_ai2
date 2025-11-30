
from engine import GameState, initial_state
from search import minimax_ab, search
from heuristics import evaluate

def select_move(state: GameState, depth: int = 3):
    """
    Unified agent:
      - if m==3 and k==3: use optimal alpha-beta (equivalent to minimax)
      - otherwise: depth-limited search using heuristic
    returns a move (row,col) or None if terminal
    """
    if state is None:
        return None
    if state.m == 3 and state.k == 3:
        return minimax_ab(state)
    return search(state, depth=depth, eval_fn=evaluate)
