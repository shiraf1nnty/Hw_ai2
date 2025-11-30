
from typing import Optional, Callable, Tuple, List
import math
from engine import GameState, actions, result, terminal, utility, player
from heuristics import evaluate

EvalFn = Callable[[GameState], float]

def _lexicographic_sorted_actions(state: GameState) -> List[Tuple[int,int]]:
    return sorted(list(actions(state)))

def order_moves(state: GameState, eval_fn: Optional[EvalFn] = None) -> List[Tuple[int,int]]:
    """
    Move ordering:
      - if eval_fn provided: shallow probe ordering by eval(result(move))
      - else: center-first heuristic (closer to center earlier), then lexicographic
    """
    acts = list(actions(state))
    if eval_fn is not None:
        scored = []
        for a in acts:
            v = eval_fn(result(state, a))
            scored.append(( -v if state.to_move == 'X' else v, a))  
        scored.sort()  
        return [a for _,a in scored]
    #center-first
    m = state.m
    center = (m - 1) / 2.0
    acts.sort(key=lambda a: (abs(a[0]-center) + abs(a[1]-center), a))
    return acts

#Plain Minimax
def minimax(state: GameState) -> Optional[Tuple[int,int]]:
    def max_value(s: GameState) -> int:
        if terminal(s): return utility(s)
        v = -math.inf
        for a in _lexicographic_sorted_actions(s):
            v = max(v, min_value(result(s,a)))
        return int(v)

    def min_value(s: GameState) -> int:
        if terminal(s): return utility(s)
        v = math.inf
        for a in _lexicographic_sorted_actions(s):
            v = min(v, max_value(result(s,a)))
        return int(v)

    if terminal(state):
        return None

    best_move = None
    best_val = -math.inf if state.to_move == 'X' else math.inf

    for a in _lexicographic_sorted_actions(state):
        child = result(state, a)
        val = min_value(child) if state.to_move == 'X' else max_value(child)
        
        if state.to_move == 'X':
            if val > best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a
        else:
            if val < best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a

    return best_move

# Alpha-Beta 
def minimax_ab(state: GameState, eval_fn: Optional[EvalFn] = None) -> Optional[Tuple[int,int]]:
    def max_value(s: GameState, alpha: float, beta: float) -> float:
        if terminal(s): return utility(s)
        v = -math.inf
        for a in order_moves(s, eval_fn):
            v = max(v, min_value(result(s,a), alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def min_value(s: GameState, alpha: float, beta: float) -> float:
        if terminal(s): return utility(s)
        v = math.inf
        for a in order_moves(s, eval_fn):
            v = min(v, max_value(result(s,a), alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
        return v

    if terminal(state):
        return None

    best_move = None
    best_val = -math.inf if state.to_move == 'X' else math.inf

    for a in order_moves(state, eval_fn):
        child = result(state, a)
        val = min_value(child, -math.inf, math.inf) if state.to_move == 'X' else max_value(child, -math.inf, math.inf)
        if state.to_move == 'X':
            if val > best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a
        else:
            if val < best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a

    return best_move

#  Depth-limited search
def search(state: GameState, depth: int, eval_fn: EvalFn) -> Optional[Tuple[int,int]]:
    """
    Depth-limited alpha-beta search returning chosen action.
    eval_fn used at depth==0 for leaf evaluation.
    """
    def max_value(s: GameState, alpha: float, beta: float, d: int) -> float:
        if terminal(s): return utility(s)
        if d == 0: return eval_fn(s)
        v = -math.inf
        for a in order_moves(s, eval_fn):
            v = max(v, min_value(result(s,a), alpha, beta, d-1))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def min_value(s: GameState, alpha: float, beta: float, d: int) -> float:
        if terminal(s): return utility(s)
        if d == 0: return eval_fn(s)
        v = math.inf
        for a in order_moves(s, eval_fn):
            v = min(v, max_value(result(s,a), alpha, beta, d-1))
            if v <= alpha: return v
            beta = min(beta, v)
        return v

    if terminal(state):
        return None

    best_move = None
    best_val = -math.inf if state.to_move == 'X' else math.inf

    for a in order_moves(state, eval_fn):
        child = result(state, a)
        val = min_value(child, -math.inf, math.inf, depth-1) if state.to_move == 'X' else max_value(child, -math.inf, math.inf, depth-1)
        if state.to_move == 'X':
            if val > best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a
        else:
            if val < best_val or (val == best_val and (best_move is None or a < best_move)):
                best_val = val; best_move = a

    return best_move



