from martypy import Marty
import deplacement
import scan
import expression
import ipaddress


def ip_valide(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    

def connection(ip):
    try:
        my_marty = Marty("wifi", ip)
        print("connexion etablie")
        return my_marty
    except Exception as e:
        print("erreure", e)
        return None


def deco(my_marty):
    my_marty.close()
    print("deconnexion")


if __name__ == '__main__':
    ip = input("Entrer l'ip du Marty : ").strip() 

    if not ip:
        ip = "192.168.0.104"
        print("ip par defaut :", ip)


    # test si ip valide
    if not ip_valide(ip):
        print("L'ip rentree n'est pas valide.")


    else:
        try:
            robot = connection(ip)


            #Si connexion reussis
            if robot:
                #On fait faire une expression pour verifier que ca marche 
                deplacement.avancer(robot,4)
                expression.enjoue(robot)
                print("Connexion etablie")

                deco(robot)
            else:
                print("Connexion echouée")

        except Exception as e:
            print("Connexion echouée (",e,")")