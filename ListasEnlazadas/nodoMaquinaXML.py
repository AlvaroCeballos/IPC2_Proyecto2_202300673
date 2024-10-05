class nodoMaquinaXML:
    def __init__(self, nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos, colaK, lineasProduccion):
        self.nombreM = nombreM
        self.cantidadLineas = cantidadLineas
        self.cantidadComponentes = cantidadComponentes
        self.tiempoEnsamblajeA = tiempoEnsamblajeA
        self.conjuntoProductos = conjuntoProductos
        self.colaK = colaK
        self.lineasProduccion = lineasProduccion
        self.siguienteMaquina = None
