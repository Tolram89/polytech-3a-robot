# bras.py

from martypy import Marty

# Angles en degrés — à ajuster après tests sur le robot
ANGLE_NEUTRE = 0
ANGLE_LEVE = 100
ANGLE_ARRIERE = -100

def lever_bras_gauche(marty: Marty):
    marty.arms(left_angle=ANGLE_LEVE, right_angle=ANGLE_NEUTRE, move_time=1000)

def lever_bras_droit(marty: Marty):
    marty.arms(left_angle=ANGLE_NEUTRE, right_angle=ANGLE_LEVE, move_time=1000)

def bras_gauche_arriere(marty: Marty):
    marty.arms(left_angle=ANGLE_ARRIERE, right_angle=ANGLE_NEUTRE, move_time=1000)

def bras_droit_arriere(marty: Marty):
    marty.arms(left_angle=ANGLE_NEUTRE, right_angle=ANGLE_ARRIERE, move_time=1000)

def position_neutre(marty: Marty):
    marty.arms(left_angle=ANGLE_NEUTRE, right_angle=ANGLE_NEUTRE, move_time=1000)

def appliquer_bras(marty: Marty, commandes: list):
    gauche = ANGLE_NEUTRE
    droite = ANGLE_NEUTRE

    for commande in commandes:
        if commande == 'ALU':
            gauche = ANGLE_LEVE
        elif commande == 'ARU':
            droite = ANGLE_LEVE
        elif commande == 'ALB':
            gauche = ANGLE_ARRIERE
        elif commande == 'ARB':
            droite = ANGLE_ARRIERE
        else:
            raise ValueError(f"Commande de bras inconnue : {commande}")

    marty.arms(left_angle=gauche, right_angle=droite, move_time=1000)