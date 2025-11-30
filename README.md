# Homework 2 — Generalized Tic-Tac-Toe (Minimax / Alpha-Beta)

## Files
- engine.py        : Game engine (initial_state, player, actions, result, winner, terminal, utility)
- heuristics.py    : Domain-specific evaluation function
- search.py        : minimax, minimax_ab, search (depth-limited + ordering)
- agent.py         : unified agent (uses AB for 3x3, depth-limited otherwise)
- tests/           : pytest test suite

## Requirements
- Python 3.8+

## Run demo (manual)
Create a small runner that uses `engine`, `agent` or call functions interactively.

## Design notes
- GameState class used for clarity and correctness.
- Deterministic tie-breaking: lexicographic (row,col).
- Minimax and Alpha-Beta return only the chosen move (as required).
- Depth-limited search uses heuristic at leaves; move ordering uses shallow probe if heuristic is provided.
- Heuristic counts open k-windows and weights immediate threats exponentially to prefer wins/blocks.

## Report 
- Explain design choices: class-based state, sliding-window k-detection, deterministic tie-break.
- Show equivalence table: minimax vs minimax_ab on several 3×3 positions.
- Show pruning effects: node counts with/without ordering (brief experiments).
- Discuss limits (large m or k explosion) and possible improvements (transposition table, iterative deepening).

## Run tests
```bash
pip install pytest
pytest -q



