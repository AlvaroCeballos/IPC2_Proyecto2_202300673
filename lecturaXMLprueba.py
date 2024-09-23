from xml.dom import minidom

class nodoActualProductoXML:
    def __init__(self, nombreProductoActual, procesoElabAct):
        self.nombreProductoActual = nombreProductoActual
        self.procesoElabAct = procesoElabAct
        self.siguienteProductoListaA = None

class listaActualProductosXML:
    def __init__(self):
        self.primerProductoListaA = None

    def insertarProductoActualListaE(self, nombreProductoActual, procesoElabAct):
        productoNuevoActualLista = nodoActualProductoXML(nombreProductoActual, procesoElabAct)
        if not self.primerProductoListaA:
            self.primerProductoListaA = productoNuevoActualLista
        else:
            productoActLista = self.primerProductoListaA
            while productoActLista.siguienteProductoListaA:
                productoActLista = productoActLista.siguienteProductoListaA
            productoActLista.siguienteProductoListaA = productoNuevoActualLista

class nodoMaquinaActualLista:
    def __init__(self, nomActualMaquina, totalLineasPactual, totalActualNodo, tiempoEnsamblajeA, listaActualProductosMaquina):
        self.nomActualMaquina = nomActualMaquina
        self.totalLineasPactual = totalLineasPactual
        self.totalActualNodo = totalActualNodo
        self.tiempoEnsamblajeA = tiempoEnsamblajeA
        self.listaActualProductosMaquina = listaActualProductosMaquina
        self.sigMaquinaLista = None

class listaMaquinasXML:
    def __init__(self):
        self.primerMlistaAct = None

    def agregarMaquinaActualNodo(self, nomActualMaquina, totalLineasPactual, totalActualNodo, tiempoEnsamblajeA, listaActualProductosMaquina):
        maquinaNuevaActual = nodoMaquinaActualLista(nomActualMaquina, totalLineasPactual, totalActualNodo, tiempoEnsamblajeA, listaActualProductosMaquina)
        if not self.primerMlistaAct:
            self.primerMlistaAct = maquinaNuevaActual
        else:
            maquinaActualLista = self.primerMlistaAct
            while maquinaActualLista.sigMaquinaLista:
                maquinaActualLista = maquinaActualLista.sigMaquinaLista
            maquinaActualLista.sigMaquinaLista = maquinaNuevaActual

def getTextContent(element, tag_name):
    tag = element.getElementsByTagName(tag_name)
    if tag:
        for node in tag:
            if node.firstChild:
                return node.firstChild.nodeValue.strip()
    return ''

def lecturaXMLActual(pathActualXML):
    try:
        parseoActualXML = minidom.parse(pathActualXML)
        raizActualXML = parseoActualXML.documentElement

        maquinasLecturaActual = raizActualXML.getElementsByTagName('Maquina')
        listaActualMaquinasLectura = listaMaquinasXML()

        for maquinaActualLexturaXML in maquinasLecturaActual:
            nomActualMaquina = getTextContent(maquinaActualLexturaXML, 'NombreMaquina')
            totalLineasPactual = int(getTextContent(maquinaActualLexturaXML, 'CantidadLineasProduccion'))
            totalActualNodo = int(getTextContent(maquinaActualLexturaXML, 'CantidadComponentes'))
            tiempoEnsamblajeA = int(getTextContent(maquinaActualLexturaXML, 'TiempoEnsamblaje'))

            productosActualesMaquinaLectura = maquinaActualLexturaXML.getElementsByTagName('Producto')
            listaActualProductosMaquina = listaActualProductosXML()

            for productoActualLect in productosActualesMaquinaLectura:
                nombreProductoActual = getTextContent(productoActualLect, 'nombre')
                procesoElabAct = getTextContent(productoActualLect, 'elaboracion')
                listaActualProductosMaquina.insertarProductoActualListaE(nombreProductoActual, procesoElabAct)

            listaActualMaquinasLectura.agregarMaquinaActualNodo(nomActualMaquina, totalLineasPactual, totalActualNodo, tiempoEnsamblajeA, listaActualProductosMaquina)

        maquinaActualLista = listaActualMaquinasLectura.primerMlistaAct
        while maquinaActualLista:
            print(f"Nombre maquina actual: {maquinaActualLista.nomActualMaquina}")
            print(f"Total actual de lineas de produccion: {maquinaActualLista.totalLineasPactual}")
            print(f"Componentes actuales: {maquinaActualLista.totalActualNodo}")
            print(f"Tiempo total: {maquinaActualLista.tiempoEnsamblajeA} minutos")
            print("Lista productos maquina actual:")
            productoActLista = maquinaActualLista.listaActualProductosMaquina.primerProductoListaA
            while productoActLista:
                print(f"Nombre actual de producto: {productoActLista.nombreProductoActual}")
                print(" Elaboracion proceso:")
                for paso in productoActLista.procesoElabAct.split():
                    print(f"  - {paso}")
                productoActLista = productoActLista.siguienteProductoListaA
            maquinaActualLista = maquinaActualLista.sigMaquinaLista

    except Exception as errorActualLectura:
        print(f"Error de lectura XML: {errorActualLectura}")

lecturaXMLActual('prueba.xml')