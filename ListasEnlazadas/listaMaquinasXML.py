
from .nodoMaquinaXML import nodoMaquinaXML


class listaMaquinasXML:
    def __init__(self):
        self.primerMaquina = None

    def InsertarMaquina(self, nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos):
        nuevaMaquina = nodoMaquinaXML(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos)
        if not self.primerMaquina:
            self.primerMaquina = nuevaMaquina
        else:
            actualMaquina = self.primerMaquina
            while actualMaquina.siguienteMaquina:
                actualMaquina = actualMaquina.siguienteMaquina
            actualMaquina.siguienteMaquina = nuevaMaquina