from xml.dom import minidom
from Maquina import Maquina
from Producto import Producto
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from ListasEnlazadas.pruebaCola import ColaElaboracion



def obtenerContextoActualLectura(elementoActualLectura, tagActualLectura):
    elementoTagA = elementoActualLectura.getElementsByTagName(tagActualLectura)
    if elementoTagA:
        for nodoActualL in elementoTagA:
            if nodoActualL.firstChild:
                return nodoActualL.firstChild.nodeValue.strip()
    return ''

def lecturaXMLActual(xmlString):
    try:
        parseoActualXML = minidom.parseString(xmlString)
        raizActualXML = parseoActualXML.documentElement

        maquinasLecturaActual = raizActualXML.getElementsByTagName('Maquina')


        for maquinaActualLexturaXML in maquinasLecturaActual:
            nombreM = obtenerContextoActualLectura(maquinaActualLexturaXML, 'NombreMaquina')
            cantidadLineas = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadLineasProduccion'))
            cantidadComponentes = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadComponentes'))
            tiempoEnsamblajeA = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'TiempoEnsamblaje'))

            productosActualesMaquinaLectura = maquinaActualLexturaXML.getElementsByTagName('Producto')
            conjuntoProductos = listaProductosXML()

            for productoActualLect in productosActualesMaquinaLectura:
                nombreProducto = obtenerContextoActualLectura(productoActualLect, 'nombre')
                elaboracion = obtenerContextoActualLectura(productoActualLect, 'elaboracion')
                conjuntoProductos.insertarProductoXML(nombreProducto, elaboracion)
                # Crear la cola de elaboración
                cola_elaboracion = ColaElaboracion()
                pasos_elaboracion = elaboracion.split()
                for paso in pasos_elaboracion:
                    linea, componente = paso.split('C')
                    linea = int(linea[1:])  # Remover 'L' y convertir a entero
                    componente = int(componente)
                    cola_elaboracion.encolar(linea, componente)
                # Verificar la cola de elaboración
                print(f"Cola de elaboración para {nombreProducto}:")
                nodo_actual = cola_elaboracion.frente
                while nodo_actual:
                    print(f"Línea: {nodo_actual.linea}, Componente: {nodo_actual.componente}")
                    nodo_actual = nodo_actual.siguiente

            listaGlobalMaquinasLectura.InsertarMaquina(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos)

        actualMaquina = listaGlobalMaquinasLectura.primerMaquina
        while actualMaquina:
            print(f"Nombre maquina actual: {actualMaquina.nombreM}")
            print(f"Total actual de lineas de produccion: {actualMaquina.cantidadLineas}")
            print(f"Componentes actuales: {actualMaquina.cantidadComponentes}")
            print(f"Tiempo en ensamblar una pieza: {actualMaquina.tiempoEnsamblajeA} segundos")
            print("Lista productos maquina actual:")
            actualProducto = actualMaquina.conjuntoProductos.primerProducto
            while actualProducto:
                print(f"Nombre actual de producto: {actualProducto.nombreProducto}")
                print(" Elaboracion proceso:")
                for paso in actualProducto.elaboracion.split():
                    print(f"  - {paso}")
                actualProducto = actualProducto.siguienteProducto
            actualMaquina = actualMaquina.siguienteMaquina

    except Exception as errorActualLectura:
        print(f"Error de lectura XML: {errorActualLectura}")

def reiniciarListaGlobal():
    global listaGlobalMaquinasLectura
    listaGlobalMaquinasLectura = listaMaquinasXML()