from .NodoCircular import NodoCircular

class listaCircular:
    def __init__(self):
        self.primero = None
        self.size = 0

    def insertar(self, dato):
        nuevo = NodoCircular(dato) 

        if self.primero == None:
            self.primero = nuevo
            self.primero.siguiente = self.primero
        else:
            actual = self.primero
            while actual.siguiente != self.primero:
                actual = actual.siguiente 
            actual.siguiente = nuevo 
            nuevo.siguiente = self.primero  
        self.size += 1

    def imprimir(self):
        actual = self.primero
        for elemento in range(self.size):
            print(actual.dato)
            actual = actual.siguiente
            elemento += 1