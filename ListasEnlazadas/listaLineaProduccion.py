from .nodoLineaProduccion import NodoLineaProduccion
from .nodoCompontente import NodoComponente

class ListaLineasProduccion:
    def __init__(self):
        self.primerLinea = None

    def insertarLinea(self, linea):
        nueva_linea = NodoLineaProduccion(linea)
        if not self.primerLinea:
            self.primerLinea = nueva_linea
        else:
            actual_linea = self.primerLinea
            while actual_linea.siguiente:
                actual_linea = actual_linea.siguiente
            actual_linea.siguiente = nueva_linea

    def insertarComponente(self, linea, componente):
        actual_linea = self.primerLinea
        while actual_linea and actual_linea.linea != linea:
            actual_linea = actual_linea.siguiente
        if actual_linea:
            nuevo_componente = NodoComponente(componente)
            nuevo_componente.linea_produccion = actual_linea
            if not actual_linea.componentes:
                actual_linea.componentes = nuevo_componente
            else:
                actual_componente = actual_linea.componentes
                while actual_componente.siguiente:
                    actual_componente = actual_componente.siguiente
                actual_componente.siguiente = nuevo_componente
                nuevo_componente.anterior = actual_componente