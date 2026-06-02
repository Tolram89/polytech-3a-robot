# expression.py

import time
from martypy import Marty

ADDON_YEUX = "eyes"

COULEUR_ETEINT = "#000000"
COULEUR_BLEU = "#0000FF"
COULEUR_ROUGE = "#FF0000"
COULEUR_VERT = "#00FF00"
COULEUR_ARC_EN_CIEL = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"]

def neutre(marty: Marty):
    marty.eyes(pose_or_angle='normal', move_time=1000)
    marty.disco_color(color=COULEUR_ETEINT, add_on=ADDON_YEUX)

def triste(marty: Marty):
    marty.eyes(pose_or_angle='wide', move_time=1000)
    marty.disco_color(color=COULEUR_BLEU, add_on=ADDON_YEUX)

def enerve(marty: Marty):
    marty.eyes(pose_or_angle='angry', move_time=1000)
    marty.disco_color(color=COULEUR_ROUGE, add_on=ADDON_YEUX)

def content(marty: Marty):
    marty.eyes(pose_or_angle='normal', move_time=1000)
    marty.disco_color(color=COULEUR_VERT, add_on=ADDON_YEUX)

def enjoue(marty: Marty):
    marty.eyes(pose_or_angle='wiggle', move_time=1000)
    for couleur in COULEUR_ARC_EN_CIEL:
        marty.disco_color(color=couleur, add_on=ADDON_YEUX)
        time.sleep(0.3)

def appliquer_expression(marty: Marty, commande: str):
    if commande == 'XNT':
        neutre(marty)
    elif commande == 'XSD':
        triste(marty)
    elif commande == 'XNG':
        enerve(marty)
    elif commande == 'XHP':
        content(marty)
    elif commande == 'XDN':
        enjoue(marty)
    else:
        raise ValueError(f"Expression inconnue : {commande}")