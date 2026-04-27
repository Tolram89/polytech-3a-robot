from martypy import Marty

print("Entrer l'ip du Marty")
ip = input()

if not ip:
    #ip part defaut
    ip = "192.168.0.101"
    print("ip par defaut : ", ip)

try:
    my_marty = Marty("wifi", ip)
    print("connexion etablie")
    
    #my_marty.dance()
    
    my_marty.close()
    print("deconnexion")
    
except Exception as e:
    print(f"erreure : {e}")

