from martypy import Marty
import deplacement


def connection(ip):
    try:
        my_marty = Marty("wifi", ip)
        print("connexion etablie")
        return my_marty
    except Exception as e:
        print(f"erreur : {e}")
        return None
    

def deco(my_marty):
    my_marty.close()
    print("deconnexion")
        


if __name__ == '__main__':
    ip = input("Entrer l'ip du Marty : ")
    if not ip:
        ip = "192.168.1.6"
        print("ip par defaut :", ip)

    robot = connection(ip)
    if robot:
        deplacement.avancer(robot, 2)
        print("test robot")
        deco(robot)



