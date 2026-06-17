# detection_couleur.py

from martypy import Marty

NOM_CAPTEUR = "LeftColorSensor"


VALEURS_REFERENCE = {
    'N': (15,  20,  10,  8),     # noir
    'P': (42,  50,  23,  36),    # mauve
    'B': (29,  28,  18,  25),    # bleu foncer
    'Y': (139, 244, 97,  52),    # jaune
    'C': (61,  54,  44,  54),    # bleu claire
    'G': (33,  40,  29,  20),    # vert
    'R': (47,  109, 17,  21),    # rouge
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
