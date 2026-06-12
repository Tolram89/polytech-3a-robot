from deplacement import deplacer
from bras import appliquer_bras, position_neutre
from expression import appliquer_expression
from detection_couleur import detecter_couleur
import http_client

def executer_choregraphie(marty, chemin):
    with open(chemin, 'r') as fichier:
        lignes = fichier.readlines()

    liste_mouvements = []
    regles_actions = {}
    partie_actuelle = "SEQ"

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne or ligne.startswith('SEQ'):
            continue

        if ligne == 'ACT':
            partie_actuelle = "ACT"
            continue

        if partie_actuelle == "SEQ":
            if ligne[0].isdigit():
                liste_mouvements.append(ligne)
        
        elif partie_actuelle == "ACT":
            elements = ligne.split()
            couleur = elements[0]    
            commandes = elements[1:]    
            regles_actions[couleur] = commandes

    print("Mouvements en mémoire :", liste_mouvements)
    print("Règles en mémoire :", regles_actions)


    reponse_serveur = http_client.start()
    
    if reponse_serveur is None:
        print("Erreur : Impossible de récupérer le MVS du serveur.")
        return
        
    limite_pas = reponse_serveur
    
    print(f"L'arbitre a validé : {limite_pas} pas maximum !")
    for tour in range(limite_pas):
        
        
        index = tour % len(liste_mouvements)
        mouvement_actuel = liste_mouvements[index] 
        
        nombre_de_pas = int(mouvement_actuel[:-1])
        direction = mouvement_actuel[-1]
        
        deplacer(marty, direction, nombre_de_pas)
        
        couleur_detectee = detecter_couleur(marty)
        
        
        commandes = regles_actions.get(couleur_detectee, [])
        

        commandes_bras = [c for c in commandes if c.startswith('A')]
        commandes_expression = [c for c in commandes if c.startswith('X')]
        
        bras_str = "+".join(commandes_bras) if commandes_bras else ""
        exp_str = commandes_expression[0] if commandes_expression else "XNT"

        http_client.step(couleur_detectee, bras_str, exp_str)
        

        if commandes_bras:
            appliquer_bras(marty, commandes_bras)
        if commandes_expression:
            appliquer_expression(marty, commandes_expression[0])