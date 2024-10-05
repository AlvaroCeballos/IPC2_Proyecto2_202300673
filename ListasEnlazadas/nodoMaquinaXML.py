class nodoMaquinaXML:
    def __init__(self, nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos, cola_elaboracion, lista_lineas_produccion):
        self.nombreM = nombreM
        self.cantidadLineas = cantidadLineas
        self.cantidadComponentes = cantidadComponentes
        self.tiempoEnsamblajeA = tiempoEnsamblajeA
        self.conjuntoProductos = conjuntoProductos
        self.cola_elaboracion = cola_elaboracion
        self.lista_lineas_produccion = lista_lineas_produccion
        self.siguienteMaquina = None
