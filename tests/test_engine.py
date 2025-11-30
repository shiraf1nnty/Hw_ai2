
import pytest
from engine import initial_state, actions, result, winner, terminal, utility

def test_actions_count_empty():
    b = initial_state(3,3)
    assert len(list(actions(b))) == 9

def test_result_and_player_switch():
    b = initial_state(3,3)
    nb = result(b, (1,1))
    assert nb.board[1][1] == 'X'
    assert nb.to_move == 'O'

def test_winner_row():
    b = initial_state(3,3)
    b = result(b, (0,0))  # X
    b = result(b, (1,0))  # O
    b = result(b, (0,1))  # X
    b = result(b, (1,1))  # O
    b = result(b, (0,2))  # X completes row
    assert winner(b) == 'X'
