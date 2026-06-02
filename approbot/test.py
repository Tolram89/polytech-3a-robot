# test.py

import pytest
from marty_mock import MartyMock
from deplacement import deplacer
from bras import appliquer_bras, position_neutre, ANGLE_NEUTRE, ANGLE_LEVE, ANGLE_ARRIERE
from expression import appliquer_expression, COULEUR_ETEINT, COULEUR_BLEU, COULEUR_ROUGE, COULEUR_VERT, COULEUR_ARC_EN_CIEL

@pytest.fixture
def marty():
    "Fournit un nouveau MartyMock pour chaque test."
    return MartyMock()


# Tests de déplacement

def test_avancer(marty):
    deplacer(marty, 'U', 2)
    assert len(marty.historique) == 1
    assert marty.historique[0]["action"] == "walk"
    assert marty.historique[0]["direction"] == "avant"
    assert marty.historique[0]["steps"] == 2

def test_reculer(marty):
    deplacer(marty, 'B', 1)
    assert marty.historique[0]["action"] == "walk"
    assert marty.historique[0]["direction"] == "arrière"

def test_gauche(marty):
    deplacer(marty, 'L', 3)
    assert marty.historique[0]["action"] == "sidestep"
    assert marty.historique[0]["side"] == "left"
    assert marty.historique[0]["steps"] == 3

def test_droite(marty):
    deplacer(marty, 'R', 1)
    assert marty.historique[0]["action"] == "sidestep"
    assert marty.historique[0]["side"] == "right"

def test_direction_inconnue(marty):
    with pytest.raises(ValueError):
        deplacer(marty, 'X', 1)


# Tests de nombre de pas 

def test_nb_pas_defaut(marty):
    "Sans préciser nb_pas, doit faire 1 pas."
    deplacer(marty, 'U')
    assert marty.historique[0]["steps"] == 1

def test_nb_pas_multiple(marty):
    deplacer(marty, 'L', 5)
    assert marty.historique[0]["steps"] == 5

# Tests des bras

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
    "Une combinaison de bras ne doit faire qu'un seul appel à arms."
    appliquer_bras(marty, ['ALU', 'ARB'])
    assert len(marty.historique) == 1

def test_appliquer_bras_neutre(marty):
    position_neutre(marty)
    assert marty.historique[0]["left_angle"] == ANGLE_NEUTRE
    assert marty.historique[0]["right_angle"] == ANGLE_NEUTRE

def test_appliquer_bras_commande_inconnue(marty):
    with pytest.raises(ValueError):
        appliquer_bras(marty, ['XXX'])

# Tests des expressions

def test_expression_neutre(marty):
    appliquer_expression(marty, 'XNT')
    assert marty.historique[0]["action"] == "eyes"
    assert marty.historique[0]["pose_or_angle"] == "normal"
    assert marty.historique[1]["action"] == "disco_color"
    assert marty.historique[1]["color"] == COULEUR_ETEINT

def test_expression_triste(marty):
    appliquer_expression(marty, 'XSD')
    assert marty.historique[0]["pose_or_angle"] == "wide"
    assert marty.historique[1]["color"] == COULEUR_BLEU

def test_expression_énerve(marty):
    appliquer_expression(marty, 'XNG')
    assert marty.historique[0]["pose_or_angle"] == "angry"
    assert marty.historique[1]["color"] == COULEUR_ROUGE

def test_expression_content(marty):
    appliquer_expression(marty, 'XHP')
    assert marty.historique[0]["pose_or_angle"] == "normal"
    assert marty.historique[1]["color"] == COULEUR_VERT

def test_expression_enjoue(marty):
    appliquer_expression(marty, 'XDN')
    assert marty.historique[0]["pose_or_angle"] == "wiggle"
    couleurs_appelees = [e["color"] for e in marty.historique[1:]]
    assert couleurs_appelees == COULEUR_ARC_EN_CIEL

def test_expression_inconnue(marty):
    with pytest.raises(ValueError):
        appliquer_expression(marty, 'XXX')