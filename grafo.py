from cola import Cola
from heap import Heap

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

class _Iterador_Lista(object):
    """Crea un iterador para Lista"""
    def __init__(self,prim):
        self.actual = prim
        self.cont = 0
    #Una referencia al primero es todo lo que se necesita
        
    def next (self):
        if self.cont == len(self.actual):
            raise StopIteration
            #En caso de que se termine la iteracion
            
        dato = self.actual[self.cont]
        #Guarda el dato
        self.cont += 1
        #Avanza en la lista
        return dato


class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.vertices = {}
        self.cantidad = 0
        self.nombre_vertices = []
        self.es_dirigido = es_dirigido

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return self.cantidad
    
   
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        iter = _Iterador_Lista(self.nombre_vertices)
        return iter
        

    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return self.nombre_vertices

    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
        if id in self.nombre_vertices:
            return self.vertices[id]["valor"]
        raise KeyError

    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
        '''
        
        if not self.vertices.has_key(id):
            self.vertices[id] = {}
            self.vertices[id]["valor"] = valor
            self.vertices[id]["adyacente"]=[]
            self.vertices[id]["cant"] = 0
            self.cantidad+=1
            self.nombre_vertices.append(id)
        else:
            self.vertices[id]["valor"] = valor



    def __delitem__(self, id):
        '''Elimina el vertice del grafo, y devuelve el valor asociado. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        if self.cantidad == 0:
            return
        if not id in self.vertices:
            raise KeyError

        for clave in self.nombre_vertices:
            
            if id in self.vertices[clave]:
                self.vertices[clave]["adyacente"].remove(id)
                del self.vertices[clave][id]
                self.vertices[clave]["cant"] -= 1
            
        self.nombre_vertices.remove(id)
        del self.vertices[id]
        self.cantidad -= 1

    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''
        return id in self.nombre_vertices
        
    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        if not desde in self.vertices or not hasta in self.vertices:
            raise KeyError
        
        self.vertices[desde]["adyacente"].append(hasta)
        self.vertices[desde]["cant"] += 1
        self.vertices[desde][hasta] = peso

        if not self.es_dirigido:
            self.vertices[hasta]["adyacente"].append(desde)
            self.vertices[hasta]["cant"] += 1
            self.vertices[hasta][desde] = peso



    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        if not desde in self.vertices or not hasta in self.vertices:
            raise KeyError
        if not hasta in self.vertices[desde]:
            raise ValueError

        self.vertices[desde]["adyacente"].remove(hasta)
        del self.vertices[desde][hasta]
        self.vertices[desde]["cant"] -= 1

        if not self.es_dirigido:
            self.vertices[hasta]["adyacente"].remove(desde)
            del self.vertices[hasta][desde]
            self.vertices[hasta]["cant"] -= 1

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if not desde in self.vertices or not hasta in self.vertices:
            raise KeyError
    
        if not hasta in self.vertices[desde]:
            raise None
        return self.vertices[desde][hasta]
            
        
    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        if not id in self.vertices:
            raise KeyError
        return self.vertices[id]["adyacente"]
    
    def bfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        if not inicio in self.vertices:
            raise KeyError
       
        (visitados, padre, orden) = crear_diccionarios(self.nombre_vertices)
        
        cola = Cola()
        cola.encolar(inicio)
        orden[inicio] = 0
        while not cola.esta_vacia():
            analizar = cola.desencolar()
            if not visitar(analizar,padre,orden,extra):
                return (padre,orden)
            dist = orden[analizar]
            if not visitados[analizar]:
                visitados[analizar] = True
            for adyacente in self.adyacentes(analizar):
                if orden[adyacente] == -1:
                    orden[adyacente] = dist + 1
                    padre[adyacente] = analizar
                    cola.encolar(adyacente)
        return (padre,orden)

    def dfs(self, visitar = visitar_nulo, extra = None, inicio=None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya 
        
        
         
        firma sea del tipo:
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        (visitados, padre, orden) = crear_diccionarios(self.nombre_vertices)
        orden[inicio] = 0
        visitados[inicio] = True
        (padre, orden) = dfs_aux(self, visitar, extra, inicio, padre, orden ,visitados)
        return (padre, orden)
        
    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''
        if self.es_dirigido:
            raise TypeError
        lista = []
        conexos = {}
        for nombre_1 in self.nombre_vertices:
            conexos[nombre_1] = 0
        for nombre in self.nombre_vertices:
            for nombre_aux in self.nombre_vertices:
                if nombre in self.vertices[nombre][nombre_aux]:
                    conexos[nombre]+=1
                    break
        for nombre_2 in self.nombre_vertices:
            if conexos[nombre_2] == 0:
                lista.append(nombre_2)

        return lista

    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        if origen in self.vertices or destino in self.vertices:
            raise KeyError
        vecinos = Heap()
        vecinos.encolar(origen, None)
        vuelta[origen] = None
        costos = {}
        costos[origen] = 0
        while not vecinos.esta_vacia() :
            actual = vecinos.desencolar()
            if actual == destino:
                break
        for adyacente in self.adyacente(actual):
            nuevo_costo = costos[actual] + self.obtener_peso_arista(actual, adyacente)
            if not adyacente in costos or nuevo_costo < costos[adyacente]:
                costos[adyacente] = nuevo_costo
                if heuristica == None:
                    vecino.encolar(adyacente,nuevo_costo)
                else:
                    vecinos.encolar(adyacente, nuevo_costo + h(adyacente))
                vuelta[adyacente] = actual
        if not destino in costos:
            return None
        return reconstruir_camino(vuelta,origen,destino)


    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        if self.es_dirigido :
            raise TypeError
        if self.vertices == []:
            return self
        visitados = {}
        grafo_mst = Grafo()
        for vertices in self.nombre_vertices:
            visitados[vertices] = False
        inicio = self.vertices[0]
        padre = None
        cant_aristas = 0
        heap = Heap()
        heap.encolar = (0, inicio, padre)
        while not heap.esta_vacio() and cant_aristas < self.cantidad - 1 :
            (peso, inicio, padre) = heap.desencolar()
            if not visitados[inicio] :
                visitados[inicio] = True
                grafo_mst.__setitem__(inicio,self.__getitem__(inicio))
                if padre != None:
                    grafo_mst.agregar_arista(padre, inicio, peso)
                cant_aristas += 1
                for adyacente in self.adyacente(inicio):
                    if not visitados[adyacente]:
                        heap.encolar(self.obtener_peso_arista(inicio,adyacente),adyacente,inicio)




def crear_diccionarios(lista_vertices):
    visitados = {}
    padre = {}
    orden = {}
    for vertices in lista_vertices:
        visitados[vertices] = False
        padre[vertices] = None
        orden[vertices] = -1
    return (visitados, padre, orden)

def dfs_aux(grafo, visitar, extra, inicio, padre, orden, visitados):
    if not visitar(inicio,padre,orden,extra):
        return (padre,orden)
    for adyacente in grafo.adyacentes(inicio):
        if not visitados[adyacente]:
            padre[adyacente] = inicio
            orden[adyacente] = orden[inicio] + 1
            dfs_aux(grafo,visitar, extra, adyacente,inicio,orden,visitados)
    return (padre,orden)

def reconstruir_camino(vuelta,origen,destino):
    recorrido = []
    padre = destino
    while padre != None:
        recorrido.insert(0,padre)
        padre = vuelta[padre]
    return recorrido

def pruebas():
    """prueba de grafos"""
    print "PRUEBAS CON GRAFO VACIO"
    grafo = Grafo()
    print "la cantidad es {}".format(len(grafo))
    print "se pudo eliminar 12 {} ".format(grafo.__delitem__("12"))
    print "12 esta el en grafo {}".format(grafo.__contains__("12"))


    print "PRUEBA CON ELEMENTOS"
    grafo.__setitem__("argentina", 1)
    grafo.__setitem__("brasil", 2)
    grafo.__setitem__("chile", 3)
    grafo.__setitem__("uruguay", 4)
    grafo.__setitem__("usa", 5)
    grafo.__setitem__("colombia", 6)
    grafo.__setitem__("peru", 7)
    grafo.agregar_arista("argentina", "brasil")
    grafo.agregar_arista("argentina", "chile")
    grafo.agregar_arista("argentina", "uruguay")
    grafo.agregar_arista("brasil", "usa")
    grafo.agregar_arista("brasil", "colombia")
    grafo.agregar_arista("chile", "peru")
    print grafo.keys()
    imprimir_vertices_y_adyacentes(grafo)
    valores_asociados(grafo)
    print "el peso de la arista de argentina a brasil {}".format(grafo.obtener_peso_arista("argentina","brasil"))
    print "argentina esta en el grafo {}".format(grafo.__contains__("argentina"))
    print "la cantidad de vertices en el grafo es {}".format(len(grafo))

#print "PRUEBA ELEMINAR ELEMENTOS"
    
    #grafo.__delitem__("argentina")
    #print "se elimino argentina"
    #imprimir_vertices_y_adyacentes(grafo)

#grafo.borrar_arista("brasil","usa")
#print "se elimino la arista entre brasil y usa"

#imprimir_vertices_y_adyacentes(grafo)


    print "PRUEBA CON ITERADOR"
    print "los vertices del grafo son:"
    for vertices in grafo:
        print vertices

    print "PRUEBA BFS"
    padre,orden = grafo.bfs(visitar_aux, None, "argentina")
    print padre
    print orden

    print "PRUEBAS DFS"
    padre_1,orden_1 = grafo.dfs(visitar_aux,None, "argentina")
    print padre_1
    print orden_1

def visitar_aux(analizar,padre,orden,extra):
    return True

def valores_asociados(grafo):
    for vertices in grafo.keys():
        print "el valor de {} son {}".format(vertices, grafo.__getitem__(vertices))

def imprimir_vertices_y_adyacentes(grafo):
    for vertices in grafo.keys():
        print "los adyacentes de {} son {}".format(vertices, grafo.adyacentes(vertices))

def main():
    pruebas()
    return 0

main()