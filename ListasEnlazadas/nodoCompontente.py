class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.ensamblar = False  # Indica si el componente debe ser ensamblado
        self.siguiente = None
        self.anterior = None