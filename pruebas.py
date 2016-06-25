import grafo



def pruebas():
    """prueba de grafos"""
    print "PRUEBAS CON GRAFO VACIO"
    grafo = Grafo()
    print "la cantidad es {}".format(len(grafo))
    grafo.__delitem__("12")
    print grafo.__contains()

def main():
    pruebas()
    return 0

main()