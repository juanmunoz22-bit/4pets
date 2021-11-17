from py2neo import Graph

def db_auth():
    graph = Graph("bolt://localhost:7687/pets")
    return graph