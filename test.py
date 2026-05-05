# test.py

import pytest
from marty_mock import MartyMock
from mouvement import deplacer

@pytest.fixture
def marty():
    """Fournit un nouveau MartyMock pour chaque test."""
    return MartyMock()


#  Tests de base 

def test_avancer(marty):
    deplacer(marty, 'U', 2)
    assert len(marty.historique) == 1
    assert marty.historique[0]["action"] == "walk"
    assert marty.historique[0]["direction"] == "avant"
    assert marty.historique[0]["num_steps"] == 2

def test_reculer(marty):
    deplacer(marty, 'B', 1)
    assert marty.historique[0]["action"] == "walk"
    assert marty.historique[0]["direction"] == "arrière"

def test_gauche(marty):
    deplacer(marty, 'L', 3)
    assert marty.historique[0]["action"] == "sidestep"
    assert marty.historique[0]["side"] == "left"
    assert marty.historique[0]["num_steps"] == 3

def test_droite(marty):
    deplacer(marty, 'R', 1)
    assert marty.historique[0]["action"] == "sidestep"
    assert marty.historique[0]["side"] == "right"

def test_direction_inconnue(marty):
    with pytest.raises(ValueError):
        deplacer(marty, 'X', 1)


#  Tests de nb_pas 

def test_nb_pas_defaut(marty):
    """Sans préciser nb_pas, doit faire 1 pas."""
    deplacer(marty, 'U')
    assert marty.historique[0]["num_steps"] == 1

def test_nb_pas_multiple(marty):
    deplacer(marty, 'L', 5)
    assert marty.historique[0]["num_steps"] == 5