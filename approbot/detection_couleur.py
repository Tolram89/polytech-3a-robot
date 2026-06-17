# detection_couleur.py

from martypy import Marty

NOM_CAPTEUR = "LeftColorSensor"


VALEURS_REFERENCE = {
    'N': (10,  10,  10,  10),    # noir
    'P': (100, 153, 50,  204),   # mauve
    'B': (60,  0,   0,   139),    # bleu foncer
    'Y': (220, 255, 220, 0),     # jaune
    'C': (200, 135, 206, 235),   # bleu claire
    'G': (120, 0,   180, 0),     # vert
    'R': (90,  220, 0,   0),     # touge
}


def lire_canaux(marty: Marty):
    clear = marty.get_color_sensor_value_by_channel(NOM_CAPTEUR, 'clear')
    red   = marty.get_color_sensor_value_by_channel(NOM_CAPTEUR, 'red')
    green = marty.get_color_sensor_value_by_channel(NOM_CAPTEUR, 'green')
    blue  = marty.get_color_sensor_value_by_channel(NOM_CAPTEUR, 'blue')
    return clear, red, green, blue


def associer_couleur(clear, red, green, blue):
    couleur_la_plus_proche = None
    ecart_minimal = None

    for couleur, (c, r, g, b) in VALEURS_REFERENCE.items():
        ecart = ((clear - c) ** 2 + (red - r) ** 2
                 + (green - g) ** 2 + (blue - b) ** 2) ** 0.5
        if ecart_minimal is None or ecart < ecart_minimal:
            ecart_minimal = ecart
            couleur_la_plus_proche = couleur

    return couleur_la_plus_proche


def detecter_couleur(marty: Marty):
    clear, red, green, blue = lire_canaux(marty)
    return associer_couleur(clear, red, green, blue)


# Noms lisibles pour guider la calibration.
NOMS_COULEURS = {
    'N': "Noir",
    'P': "Mauve",
    'B': "Bleu foncé",
    'Y': "Jaune",
    'C': "Bleu ciel",
    'G': "Vert",
    'R': "Rouge",
}


def calibrer(marty: Marty, nb_mesures: int = 5):
    """Calibre les couleurs une par une et affiche le VALEURS_REFERENCE à copier.

    Pour chaque couleur : pose le robot sur la pastille, appuie sur Entrée.
    On fait la moyenne de `nb_mesures` lectures pour plus de stabilité.
    """
    nouvelles_valeurs = {}

    for code, nom in NOMS_COULEURS.items():
        input(f"\nPlace le robot sur la couleur {nom} ({code}) puis appuie sur Entrée...")

        sommes = [0, 0, 0, 0]
        for _ in range(nb_mesures):
            canaux = lire_canaux(marty)
            for i in range(4):
                sommes[i] += canaux[i]

        moyennes = tuple(round(s / nb_mesures) for s in sommes)
        nouvelles_valeurs[code] = moyennes
        print(f"  → {nom} ({code}) : {moyennes}")

    print("\nCalibration terminée. Copie ce dictionnaire dans VALEURS_REFERENCE :\n")
    print("VALEURS_REFERENCE = {")
    for code, valeurs in nouvelles_valeurs.items():
        print(f"    '{code}': {valeurs},  # {NOMS_COULEURS[code]}")
    print("}")

    return nouvelles_valeurs
