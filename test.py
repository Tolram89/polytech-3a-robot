# test.py

import pytest
from marty_mock import MartyMock
from deplacement import deplacer
from bras import appliquer_bras, position_neutre, ANGLE_NEUTRE, ANGLE_LEVE, ANGLE_ARRIERE

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

    # --- Tests bras ---

def test_appliquer_bras_gauche_leve(marty):
    appliquer_bras(marty, ['ALU'])
    assert marty.historique[0]["action"] == "arms"
    assert marty.historique[0]["left_angle"] == ANGLE_LEVE
    assert marty.historique[0]["right_angle"] == ANGLE_NEUTRE

def test_appliquer_bras_droit_leve(marty):
    appliquer_bras(marty, ['ARU'])
    assert marty.historique[0]["left_angle"] == ANGLE_NEUTRE
    assert marty.historique[0]["right_angle"] == ANGLE_LEVE

def test_appliquer_bras_gauche_arriere(marty):
    appliquer_bras(marty, ['ALB'])
    assert marty.historique[0]["left_angle"] == ANGLE_ARRIERE
    assert marty.historique[0]["right_angle"] == ANGLE_NEUTRE

def test_appliquer_bras_droit_arriere(marty):
    appliquer_bras(marty, ['ARB'])
    assert marty.historique[0]["left_angle"] == ANGLE_NEUTRE
    assert marty.historique[0]["right_angle"] == ANGLE_ARRIERE

def test_appliquer_bras_combinaison(marty):
    appliquer_bras(marty, ['ALU', 'ARB'])
    assert marty.historique[0]["left_angle"] == ANGLE_LEVE
    assert marty.historique[0]["right_angle"] == ANGLE_ARRIERE

def test_appliquer_bras_un_seul_appel(marty):
    """Une combinaison de bras ne doit faire qu'un seul appel à arms."""
    appliquer_bras(marty, ['ALU', 'ARB'])
    assert len(marty.historique) == 1

def test_appliquer_bras_neutre(marty):
    position_neutre(marty)
    assert marty.historique[0]["left_angle"] == ANGLE_NEUTRE
    assert marty.historique[0]["right_angle"] == ANGLE_NEUTRE

def test_appliquer_bras_commande_inconnue(marty):
    with pytest.raises(ValueError):
        appliquer_bras(marty, ['XXX'])