from xml.dom import minidom
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from ListasEnlazadas.pruebaCola import ColaElaboracion
from ListasEnlazadas.listaLineaProduccion import ListaLineasProduccion
import xml.etree.ElementTree as ET
import os

listaGlobalMaquinasLectura = listaMaquinasXML()

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

        # Crear el elemento raíz del HTML
        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        title = ET.SubElement(head, 'title')
        title.text = 'Maquinas'
        body = ET.SubElement(html, 'body')
        table = ET.SubElement(body, 'table', border='1')

        # Crear la fila de encabezado
        header = ET.SubElement(table, 'tr')
        th = ET.SubElement(header, 'th')
        th.text = 'Nombre Maquina'
        th = ET.SubElement(header, 'th')
        th.text = 'Cantidad Lineas'
        th = ET.SubElement(header, 'th')
        th.text = 'Cantidad Componentes'
        th = ET.SubElement(header, 'th')
        th.text = 'Tiempo Ensamblaje'
        th = ET.SubElement(header, 'th')
        th.text = 'Productos'

        for maquinaActualLexturaXML in maquinasLecturaActual:
            nombreM = obtenerContextoActualLectura(maquinaActualLexturaXML, 'NombreMaquina')
            cantidadLineas = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadLineasProduccion'))
            cantidadComponentes = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadComponentes'))
            tiempoEnsamblajeA = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'TiempoEnsamblaje'))

            productosActualesMaquinaLectura = maquinaActualLexturaXML.getElementsByTagName('Producto')
            conjuntoProductos = listaProductosXML()

            productos_td = ET.Element('td')
            for productoActualLect in productosActualesMaquinaLectura:
                nombreProducto = obtenerContextoActualLectura(productoActualLect, 'nombre')
                elaboracion = obtenerContextoActualLectura(productoActualLect, 'elaboracion')
                conjuntoProductos.insertarProductoXML(nombreProducto, elaboracion)
                productos_td.append(ET.Element('br'))
                productos_td.text = (productos_td.text or '') + f"{nombreProducto} ({elaboracion})"

                # Crear la cola de elaboración
                cola_elaboracion = ColaElaboracion()
                pasos_elaboracion = elaboracion.split()
                for paso in pasos_elaboracion:
                    cola_elaboracion.encolar(paso)  # Encolar L#C# como una sola cadena

                # Crear la lista de listas para las líneas de producción y componentes
                segundoActual = 0
                lista_lineas_produccion = ListaLineasProduccion()
                nodo_actual = cola_elaboracion.frente
                while nodo_actual:
                    linea, componente = nodo_actual.paso.split('C')
                    linea = int(linea[1:])  # Remover 'L' y convertir a entero
                    componente = int(componente)
                    lista_lineas_produccion.insertarLinea(linea)
                    lista_lineas_produccion.insertarComponente(linea, componente, cantidadComponentes, segundoActual)
                    nodo_actual = nodo_actual.siguiente

                while not lista_lineas_produccion.todasListasRecorridas():
                    segundoActual += 1
                    lista_lineas_produccion.avanzarSegundo(segundoActual)

            listaGlobalMaquinasLectura.InsertarMaquina(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos, cola_elaboracion, lista_lineas_produccion)

            # Crear una fila en la tabla HTML
            row = ET.SubElement(table, 'tr')
            ET.SubElement(row, 'td').text = nombreM
            ET.SubElement(row, 'td').text = str(cantidadLineas)
            ET.SubElement(row, 'td').text = str(cantidadComponentes)
            ET.SubElement(row, 'td').text = str(tiempoEnsamblajeA)
            row.append(productos_td)

        # Convertir el árbol de elementos a una cadena
        html_str = ET.tostring(html, encoding='unicode', method='html')

        # Escribir el HTML a un archivo
        with open('maquinas.html', 'w', encoding='utf-8') as file:
            file.write(html_str)

        # Abrir el archivo HTML automáticamente
        os.startfile('maquinas.html')

    except Exception as errorActualLectura:
        print(f"Error de lectura XML: {errorActualLectura}")

def reiniciarListaGlobal():
    global listaGlobalMaquinasLectura
    listaGlobalMaquinasLectura = listaMaquinasXML()