# detection_couleur.py

from martypy import Marty

NOM_CAPTEUR = "LeftColorSensor"

# Valeurs brutes de référence pour chaque couleur, à calibrer sur le vrai robot
VALEURS_REFERENCE = {
    'N': 10,   # Noir
    'P': 80,   # Violet
    'B': 50,   # Bleu
    'Y': 200,  # Jaune
    'C': 120,  # Cyan
    'G': 150,  # Vert
    'R': 170,  # Rouge
}

def lire_valeur_brute(marty: Marty):
    return marty.get_ground_sensor_reading(NOM_CAPTEUR)

def associer_couleur(valeur_brute: int):
    couleur_la_plus_proche = None
    ecart_minimal = None

    for couleur, valeur_ref in VALEURS_REFERENCE.items():
        ecart = abs(valeur_brute - valeur_ref)
        if ecart_minimal is None or ecart < ecart_minimal:
            ecart_minimal = ecart
            couleur_la_plus_proche = couleur

    return couleur_la_plus_proche

def detecter_couleur(marty: Marty):
    valeur_brute = lire_valeur_brute(marty)
    return associer_couleur(valeur_brute)