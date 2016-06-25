class Nodo (object):
    """Representa a un objecto con las caracteristicas de un Nodo"""
    def __init__(self,dato = None, prox = None):
        self.dato = dato
        self.prox = prox
        
    def __str__(self):
        return str (self.dato)

class Cola(object):
	"""Define una instancia de la clase colas implementadas con listas enlazadas"""
	def __init__ (self):
		self.primero = None
		self.ultimo = None
		#Crea una Cola vacia

	def encolar (self,dato):
        
		nodo = Nodo(dato)
		if (self.esta_vacia()):
			self.primero = nodo
			self.ultimo = nodo
			#En caso de estar vacia, el ultimo y el primero es el nodo que se crea.
			return
		self.ultimo.prox = nodo
		self.ultimo = nodo

	def desencolar (self):
        
		if self.primero:
		#Si existe el primero
			dato = self.primero.dato
			#Guarda el dato a borrar
			self.primero = self.primero.prox
			#Saca la referencia del primero, eliminandolo y hace que el segundo sea el primero
			if not self.primero: 
			#Si ese segundo pasa a ser None
				self.ultimo = None 
				#Si el primero es None, el ultimo tambien.
			return dato
		else:
			raise ValueError ("No se puede desencolar")		
	
	def esta_vacia (self):
       		return self.primero == None and self.ultimo == None
