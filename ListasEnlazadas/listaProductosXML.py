from .nodoProductoXML import nodoProductoXML

class listaProductosXML:
    def __init__(self):
        self.primerProducto = None

    def insertarProductoXML(self, nombreProducto, elaboracion):
        nuevoProducto = nodoProductoXML(nombreProducto, elaboracion)
        if not self.primerProducto:
            self.primerProducto = nuevoProducto
        else:
            actualProducto = self.primerProducto
            while actualProducto.siguienteProducto:
                actualProducto = actualProducto.siguienteProducto
            actualProducto.siguienteProducto = nuevoProducto