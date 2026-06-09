import conn

def get_batterie(my_marty):
    try:
        pourcentage = my_marty.get_battery_remaining()
        return pourcentage
    except Exception as e:
        print("erreure batterie" , e)
        return None
    
    
if __name__ == '__main__':
    robot = conn.connection("192.168.0.103")
    if robot:
        batterie = get_batterie(robot)
        print("Le robot a ", batterie , " %")
        conn.deco(robot)
