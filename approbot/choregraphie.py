from martypy import Marty
from deplacement import deplacer
from bras import appliquer_bras, position_neutre
from expression import appliquer_expression
from detection_couleur import detecter_couleur

def executer_choregraphie(marty, chemin):

    with open(chemin, 'r') as fichier:
        lignes = fichier.readlines()

    i = 0
    while i < len(lignes):
        ligne = lignes[i].strip()

        if not ligne:
            i += 1
            continue

        if ligne.startswith('SEQ'):
            i += 1

        elif ligne[0].isdigit():
            nombre_de_pas = int(ligne[:-1])
            direction = ligne[-1]
            deplacer(marty, direction, nombre_de_pas)
            i += 1

        elif ligne == 'ACT':
            couleur = detecter_couleur(marty)
            i += 1

            while i < len(lignes):
                ligne = lignes[i].strip()
                if not ligne:
                    i += 1
                    continue
                elements = ligne.split()
                if elements[0] == couleur:
                    commandes = elements[1:]
                    commandes_bras = [c for c in commandes if c.startswith('A')]
                    commandes_expression = [c for c in commandes if c.startswith('X')]
                    if commandes_bras:
                        appliquer_bras(marty, commandes_bras)
                    if commandes_expression:
                        appliquer_expression(marty, commandes_expression[0])
                    break
                i += 1

            position_neutre(marty)
            i += 1

        else:
            i += 1