class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.ensamblar = False  # Indica si el componente debe ser ensamblado
        self.segundoActual = 0  # Inicializa el tiempo actual en 0
        self.siguiente = None
        self.anterior = None