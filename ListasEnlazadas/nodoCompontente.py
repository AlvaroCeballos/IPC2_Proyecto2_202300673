class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.ensamblar = False
        self.segundoActual = 0
        self.siguiente = None
        self.anterior = None