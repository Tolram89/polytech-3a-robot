import martypy

robots_trouves = martypy.ClientMV2.discover(None)
print(robots_trouves)
print(type(robots_trouves))