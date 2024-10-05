from .nodoCola import NodoElaboracion

class ColaElaboracion:
    def __init__(self):
        self.frente = None
        self.final = None

    def insertarCola(self, paso):
        nuevo_nodo = NodoElaboracion(paso)
        if not self.frente:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

    def kCOla(self):
        if not self.frente:
            return None
        nodo = self.frente
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return nodo

    def empty(self):
        return self.frente is None