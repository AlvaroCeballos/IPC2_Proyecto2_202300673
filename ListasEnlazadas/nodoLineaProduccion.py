
class NodoLineaProduccion:
    def __init__(self, linea):
        self.linea = linea
        self.componentes = None  # Apunta a la lista doblemente enlazada de componentes
        self.siguiente = None