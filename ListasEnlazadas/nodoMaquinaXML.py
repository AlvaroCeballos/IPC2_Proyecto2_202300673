class nodoMaquinaXML:
    def __init__(self, nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos):
        self.nombreM = nombreM
        self.cantidadLineas = cantidadLineas
        self.cantidadComponentes = cantidadComponentes
        self.tiempoEnsamblajeA = tiempoEnsamblajeA
        self.conjuntoProductos = conjuntoProductos
        self.siguienteMaquina = None
