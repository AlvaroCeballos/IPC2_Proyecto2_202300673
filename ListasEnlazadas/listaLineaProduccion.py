from .nodoLineaProduccion import NodoLineaProduccion
from .nodoCompontente import NodoComponente

class ListaLineasProduccion:
    def __init__(self):
        self.primerLinea = None

    def insertarLinea(self, linea):
        # Validacion de linea de produccion existente
        actualLinea = self.primerLinea
        while actualLinea:
            if actualLinea.linea == linea:
                return 
            actualLinea = actualLinea.siguiente

        nuevaLinea = NodoLineaProduccion(linea)
        if not self.primerLinea:
            self.primerLinea = nuevaLinea
        else:
            actualLinea = self.primerLinea
            while actualLinea.siguiente:
                actualLinea = actualLinea.siguiente
            actualLinea.siguiente = nuevaLinea

    def insertarComponente(self, linea, componente, cantComponente, segundoActual):
        actualLinea = self.primerLinea
        while actualLinea and actualLinea.linea != linea:
            actualLinea = actualLinea.siguiente
        if actualLinea:
            if not actualLinea.componentes:
                for i in range(1, cantComponente + 1):
                    nuevoComponente = NodoComponente(i)
                    if not actualLinea.componentes:
                        actualLinea.componentes = nuevoComponente
                    else:
                        componenteActual = actualLinea.componentes
                        while componenteActual.siguiente:
                            componenteActual = componenteActual.siguiente
                        componenteActual.siguiente = nuevoComponente
                        nuevoComponente.anterior = componenteActual

            componenteActual = actualLinea.componentes
            while componenteActual:
                if componenteActual.componente == componente:
                    componenteActual.ensamblar = True
                    componenteActual.segundoActual = segundoActual
                componenteActual = componenteActual.siguiente

    def avanzarSegundo(self, segundo):
        actualLinea = self.primerLinea
        while actualLinea:
            componenteActual = actualLinea.componentes
            contador = 1
            while componenteActual:
                if contador == segundo:
                    componenteActual.segundoActual = segundo
                componenteActual = componenteActual.siguiente
                contador += 1
            actualLinea = actualLinea.siguiente

    def todasListasRecorridas(self):
        actualLinea = self.primerLinea
        while actualLinea:
            componenteActual = actualLinea.componentes
            while componenteActual:
                if componenteActual.segundoActual == 0:
                    return False
                componenteActual = componenteActual.siguiente
            actualLinea = actualLinea.siguiente
        return True
                