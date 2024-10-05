from .nodoLineaProduccion import NodoLineaProduccion
from .nodoCompontente import NodoComponente

class ListaLineasProduccion:
    def __init__(self):
        self.primerLinea = None

    def insertarLinea(self, linea):
        # Verificar si la línea ya existe
        actual_linea = self.primerLinea
        while actual_linea:
            if actual_linea.linea == linea:
                return  # La línea ya existe, no hacer nada
            actual_linea = actual_linea.siguiente

        # Si la línea no existe, crear una nueva
        nueva_linea = NodoLineaProduccion(linea)
        if not self.primerLinea:
            self.primerLinea = nueva_linea
        else:
            actual_linea = self.primerLinea
            while actual_linea.siguiente:
                actual_linea = actual_linea.siguiente
            actual_linea.siguiente = nueva_linea

    def insertarComponente(self, linea, componente, total_componentes, segundoActual):
        actual_linea = self.primerLinea
        while actual_linea and actual_linea.linea != linea:
            actual_linea = actual_linea.siguiente
        if actual_linea:
            # Crear todos los nodos necesarios solo si no existen
            if not actual_linea.componentes:
                for i in range(1, total_componentes + 1):
                    nuevo_componente = NodoComponente(i)
                    if not actual_linea.componentes:
                        actual_linea.componentes = nuevo_componente
                    else:
                        actual_componente = actual_linea.componentes
                        while actual_componente.siguiente:
                            actual_componente = actual_componente.siguiente
                        actual_componente.siguiente = nuevo_componente
                        nuevo_componente.anterior = actual_componente

            # Marcar el componente que debe ser ensamblado y asignar segundoActual
            actual_componente = actual_linea.componentes
            while actual_componente:
                if actual_componente.componente == componente:
                    actual_componente.ensamblar = True
                    actual_componente.segundoActual = segundoActual
                actual_componente = actual_componente.siguiente

    def avanzarSegundo(self, segundo):
        actual_linea = self.primerLinea
        while actual_linea:
            actual_componente = actual_linea.componentes
            contador = 1
            while actual_componente:
                if contador == segundo:
                    actual_componente.segundoActual = segundo
                actual_componente = actual_componente.siguiente
                contador += 1
            actual_linea = actual_linea.siguiente

    def todasListasRecorridas(self):
        actual_linea = self.primerLinea
        while actual_linea:
            actual_componente = actual_linea.componentes
            while actual_componente:
                if actual_componente.segundoActual == 0:
                    return False
                actual_componente = actual_componente.siguiente
            actual_linea = actual_linea.siguiente
        return True
                