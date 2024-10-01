class NodoComponente:
    def __init__(self, componente):
        self.componente = componente
        self.siguiente = None
        self.anterior = None
        self.linea_produccion = None  # Apunta a la línea de producción correspondiente