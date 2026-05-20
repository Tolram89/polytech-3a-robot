import subprocess
import concurrent.futures
import martypy


BASE_IP = "192.168.0." 
TIMEOUT_MS = "200"     

def ping_ip(ip):
    """Envoie un ping à une IP. Retourne l'IP si elle répond, sinon None."""
    
    commande = ['ping', '-n', '2', '-w', TIMEOUT_MS, ip]
    
    resultat = subprocess.run(commande, capture_output=True, text=True)
    
    
    if "TTL=" in resultat.stdout:
        return ip
    return None

def scanner_reseau():
    print(f"Lancement du radar sur {BASE_IP}x ...")
    machines_actives = []
    
    
    ips_a_tester = [f"{BASE_IP}{i}" for i in range(2, 254)]
    
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        
        resultats = executor.map(ping_ip, ips_a_tester)
        
        for ip in resultats:
            if ip is not None:
                machines_actives.append(ip)
                
    return machines_actives

def vrai_robot(ip_trouvees) :
    vrai_robot =[]    
    for ip in ip_trouvees :
        try :
            martypy.Marty("wifi",ip)
            vrai_robot.append(ip)
        except Exception as e:
            print(f"l'ip {ip} ne correspond pas à un robot")
    return vrai_robot

if __name__ == "__main__":
    ips_trouvees = scanner_reseau()
    print(f"\n {len(ips_trouvees)} machines détectées sur le réseau :")
    for ip in ips_trouvees:
        print(f" - {ip}")
    ip_robot= vrai_robot(ips_trouvees)
    print(f"\n {len(ip_robot)} robots trouvés sur le réseau :")
    for ip in ip_robot:
        print(f" - {ip}")