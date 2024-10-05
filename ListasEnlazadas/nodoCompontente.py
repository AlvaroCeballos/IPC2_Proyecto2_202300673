class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.ensamblar = False
        self.siguiente = None
        self.anterior = None
        self.segundoActual = 0