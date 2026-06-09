# dance_parser.py

def charger_fichier_dance(chemin: str):

    with open(chemin, 'r') as fichier:
        lignes = fichier.readlines()

    mouvements = []
    actions_par_couleur = {}

    # On repère la ligne "ACT" qui sépare les deux sections
    index_act = None
    for i, ligne in enumerate(lignes):
        if ligne.strip() == 'ACT':
            index_act = i
            break

    if index_act is None:
        raise ValueError("Le fichier .dance ne contient pas de section ACT.")

    # on ignore la première ligne "SEQ"
    for ligne in lignes[1:index_act]:
        ligne = ligne.strip()
        if not ligne:
            continue
        nombre_de_pas = int(ligne[:-1])
        direction = ligne[-1]
        mouvements.append((nombre_de_pas, direction))

    for ligne in lignes[index_act + 1:]:
        ligne = ligne.strip()
        if not ligne:
            continue
        elements = ligne.split()
        couleur = elements[0]
        commandes = elements[1:]
        actions_par_couleur[couleur] = commandes

    return {
        'mouvements': mouvements,
        'actions_par_couleur': actions_par_couleur,
    }