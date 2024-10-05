from flask import Flask, render_template, request, url_for, redirect, flash, send_file
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from ListasEnlazadas.pruebaCola import ColaElaboracion
from ListasEnlazadas.listaLineaProduccion import ListaLineasProduccion
from xml.dom import minidom
import graphviz

app = Flask(__name__)
app.secret_key = 'pruebaClaveSuperSegura'

listaGlobalMaquinasLectura = listaMaquinasXML()

@app.route('/LeerXML')
def leer():
    return render_template('subirXML.html')

@app.route('/lecturaXML', methods=['POST'])
def lecturaXML():
    try:
        if 'xmlFile' not in request.files:
            flash("No se encontró el archivo XML", "error")
            return redirect(url_for('leer'))
        
        file = request.files['xmlFile']
        
        if file.filename == '':
            flash("Por favor seleccionar un archivo XML", "error")
            return redirect(url_for('leer'))
        
        if file and file.filename.endswith('.xml'):
            xmlString = file.read().decode('utf-8')
            lecturaXMLActual(xmlString)
            flash("Archivo XML leído correctamente", "success")
            return redirect(url_for('leer'))
        else:
            flash("Por favor seleccionar un archivo XML válido", "error")
            return redirect(url_for('leer'))
    except Exception as e:
        flash(f"Error al leer el archivo XML: {e}", "error")
        return redirect(url_for('leer'))

@app.route('/buscarProducto', methods=['GET', 'POST'])
def buscarProducto():
    if request.method == 'POST':
        nombreProducto = request.form['nombreProducto']
        producto = buscarProductoEnMaquinas(nombreProducto)
        if producto:
            tabla_html = producto.tabla_html
        else:
            flash("Producto no encontrado", "error")
            tabla_html = ""
        return render_template('archivosSalida.html', tabla_html=tabla_html)
    return render_template('archivosSalida.html', tabla_html="")

@app.route('/generarCola', methods=['POST'])
def generarCola():
    nombreProducto = request.form['nombreProducto']
    producto = buscarProductoEnMaquinas(nombreProducto)
    if producto:
        dot = graphviz.Digraph(comment='Cola de Elaboración')
        nodo_actual = producto.cola_elaboracion.frente
        while nodo_actual:
            dot.node(str(nodo_actual), nodo_actual.paso)
            if nodo_actual.siguiente:
                dot.edge(str(nodo_actual), str(nodo_actual.siguiente))
            nodo_actual = nodo_actual.siguiente
        dot.render('cola_elaboracion.gv', view=False)
        return send_file('cola_elaboracion.gv.pdf', as_attachment=True)
    else:
        flash("Producto no encontrado", "error")
        return redirect(url_for('buscarProducto'))

@app.route('/borrarDatos', methods=['POST'])
def borrarDatos():
    reiniciarListaGlobal()  
    flash("Programa inicializado correctamente", "success")
    return redirect('/')

@app.route('/')
def listar():
    return render_template('index.html')

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

                print(f"Producto a ensamblar: {nombreProducto}")

                while not lista_lineas_produccion.todasListasRecorridas():
                    segundoActual += 1
                    lista_lineas_produccion.avanzarSegundo(segundoActual)
                    
                    # Verificar la lista de listas
                    print(f"Segundo {segundoActual}:")
                    actual_linea = lista_lineas_produccion.primerLinea
                    while actual_linea:
                        print(f"Línea {actual_linea.linea}:")
                        actual_componente = actual_linea.componentes
                        contador = 1
                        while actual_componente:
                            if actual_componente.segundoActual == segundoActual:
                                ensamblar_str = " (ensamblar)" if actual_componente.ensamblar else ""
                                print(f"  Componente: {actual_componente.componente}{ensamblar_str}")
                                break
                            actual_componente = actual_componente.siguiente
                            contador += 1
                        actual_linea = actual_linea.siguiente

                # Generar la tabla HTML para el producto
                tabla_html = generarTablaHTML(lista_lineas_produccion)
                # Asignar la tabla HTML al producto actual
                producto_nodo = conjuntoProductos.primerProducto
                while producto_nodo:
                    if producto_nodo.nombreProducto == nombreProducto:
                        producto_nodo.tabla_html = tabla_html
                        producto_nodo.cola_elaboracion = cola_elaboracion  # Asignar la cola de elaboración
                        break
                    producto_nodo = producto_nodo.siguienteProducto

            listaGlobalMaquinasLectura.InsertarMaquina(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos, cola_elaboracion, lista_lineas_produccion)

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

def buscarProductoEnMaquinas(nombreProducto):
    actualMaquina = listaGlobalMaquinasLectura.primerMaquina
    while actualMaquina:
        actualProducto = actualMaquina.conjuntoProductos.primerProducto
        while actualProducto:
            if actualProducto.nombreProducto == nombreProducto:
                return actualProducto
            actualProducto = actualProducto.siguienteProducto
        actualMaquina = actualMaquina.siguienteMaquina
    return None

def generarTablaHTML(lista_lineas_produccion):
    tabla = "<table class='min-w-full bg-white'>"
    tabla += "<thead><tr><th class='py-2'>Tiempo</th>"
    
    actualLinea = lista_lineas_produccion.primerLinea
    while actualLinea:
        tabla += f"<th class='py-2'>Línea {actualLinea.linea}</th>"
        actualLinea = actualLinea.siguiente
    tabla += "</tr></thead><tbody>"

    max_segundo = 0
    actualLinea = lista_lineas_produccion.primerLinea
    while actualLinea:
        componente = actualLinea.componentes
        while componente:
            if componente.segundoActual > max_segundo:
                max_segundo = componente.segundoActual
            componente = componente.siguiente
        actualLinea = actualLinea.siguiente

    for segundo in range(1, max_segundo + 1):
        tabla += f"<tr class='bg-gray-100'><td class='border px-4 py-2'>{segundo}s</td>"
        actualLinea = lista_lineas_produccion.primerLinea
        while actualLinea:
            componente = actualLinea.componentes
            encontrado = False
            while componente:
                if componente.segundoActual == segundo:
                    tabla += f"<td class='border px-4 py-2'>{componente.componente}"
                    if componente.ensamblar:
                        tabla += " (Ensamblar)"
                    tabla += "</td>"
                    encontrado = True
                    break
                componente = componente.siguiente
            if not encontrado:
                tabla += "<td class='border px-4 py-2'>No hace nada</td>"
            actualLinea = actualLinea.siguiente
        tabla += "</tr>"
    tabla += "</tbody></table>"
    return tabla

if __name__ == '__main__':
    slc = 0
    listaDoble = ListaEnlazadaDoble()
    app.run(debug=True)