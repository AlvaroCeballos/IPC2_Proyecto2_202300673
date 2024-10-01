from .nodoCola import NodoElaboracion

class ColaElaboracion:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, linea, componente):
        nuevo_nodo = NodoElaboracion(linea, componente)
        if not self.frente:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

    def desencolar(self):
        if not self.frente:
            return None
        nodo = self.frente
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return nodo

    def esta_vacia(self):
        return self.frente is None