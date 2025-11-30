
from engine import winner

def evaluate(state):
    w = winner(state)
    if w == 'X': return 10000
    if w == 'O': return -10000

    score = 0
    b = state.board
    m = state.m
    k = state.k

    # count open lines
    def score_line(cells):
        if 'X' in cells and 'O' in cells:
            return 0
        if cells.count('X') > 0:
            return cells.count('X')
        if cells.count('O') > 0:
            return -cells.count('O')
        return 0

    # rows
    for r in range(m):
        score += score_line(b[r])
    # cols
    for c in range(m):
        col = [b[r][c] for r in range(m)]
        score += score_line(col)

    return score
