from martypy import Marty

def avancer(marty: Marty, nb_pas: int = 1):
    #25 pour longueur de pas en mm, et 1000 pour tps en ms pour faire un pas
    marty.walk(num_steps=nb_pas, step_length=25, move_time=1500)

def reculer(marty: Marty, nb_pas: int = 1):
    marty.walk(num_steps=nb_pas, step_length=-25, move_time=1500)

def gauche(marty: Marty, nb_pas: int = 1):
    marty.sidestep(side='left', num_steps = nb_pas, move_time=1500)

def droite(marty: Marty, nb_pas: int = 1):
    marty.sidestep(side='right', num_steps = nb_pas, move_time=1500)

def deplacer(marty: Marty, direction: str, nb_pas: int = 1):
    if direction == 'U':
        avancer(marty, nb_pas)
    elif direction == 'B':
        reculer(marty, nb_pas)
    elif direction == 'L':
        gauche(marty, nb_pas)
    elif direction == 'R':
        droite(marty, nb_pas)
    else:
        raise ValueError(f"Direction inconnue : {direction}")
