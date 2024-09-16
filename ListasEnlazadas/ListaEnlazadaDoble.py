from .NodoDoble import NodoDoble
class ListaDEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def insertar(self, dato):
        nuevo = NodoDoble(dato)
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo 
            nuevo.anterior = self.ultimo 
            self.ultimo = nuevo 
        self.size += 1

    def datoReversa(self):
        actual = self.ultimo
        while actual != None:
            print(actual.dato)
            actual = actual.anterior