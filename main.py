from flask import Flask, render_template, request, url_for, redirect, flash, send_file, Response
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from ListasEnlazadas.pruebaCola import ColaElaboracion
from ListasEnlazadas.listaLineaProduccion import ListaLineasProduccion
from xml.dom import minidom
import graphviz
import os

app = Flask(__name__)
app.secret_key = 'claveSeguraIPC2$$$$$'

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
            tabla = producto.tablaC
        else:
            flash("Ingrese correctamente el nombre del producto", "error")
            tabla = ""
        return render_template('archivosSalida.html', tablaC=tabla)
    return render_template('archivosSalida.html', tablaC="")

@app.route('/generarCola', methods=['POST'])
def generarCola():
    nombreProducto = request.form['nombreProducto']
    producto = buscarProductoEnMaquinas(nombreProducto)
    if producto:
        dot = graphviz.Digraph(comment='Cola')
        actual = producto.colaK.frente
        while actual:
            dot.node(str(actual), actual.paso)
            if actual.siguiente:
                dot.edge(str(actual), str(actual.siguiente))
            actual = actual.siguiente
        dot.render('colaK.gv', view=False)
        return send_file('colaK.gv.pdf', as_attachment=True)
    else:
        flash("Ingrese correctamente el nombre del producto", "error")
        return redirect(url_for('buscarProducto'))

@app.route('/exportarHTML', methods=['POST'])
def exportarHTML():
    nombreProducto = request.form['nombreProducto']
    producto = buscarProductoEnMaquinas(nombreProducto)
    if producto:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Exportación de Tabla</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mx-auto p-4">
                <h1 class="text-2xl font-bold mb-4">Tabla de {nombreProducto}</h1>
                {producto.tablaC}
            </div>
        </body>
        </html>
        """
        file_path = f"{nombreProducto}_tabla.html"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        return send_file(file_path, as_attachment=True)
    else:
        flash("Ingrese correctamente el nombre del producto", "error")
        return redirect(url_for('buscarProducto'))

@app.route('/exportarXML', methods=['GET'])
def exportarXML():
    try:
        xml_content = generarXMLProductos()
        return Response(xml_content, mimetype='application/xml', headers={"Content-Disposition": "attachment;filename=productos.xml"})
    except Exception as e:
        flash(f"Error al exportar el archivo XML: {e}", "error")
        return redirect(url_for('listar'))

@app.route('/borrarDatos', methods=['POST'])
def borrarDatos():
    reiniciarListaGlobal()  
    flash("Programa inicializado correctamente", "success")
    return redirect('/')

@app.route('/')
def listar():
    return render_template('index.html')

def inicializacionParametroXML(elementoActualLectura, tagActualLectura):
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
            nombreM = inicializacionParametroXML(maquinaActualLexturaXML, 'NombreMaquina')
            cantidadLineas = int(inicializacionParametroXML(maquinaActualLexturaXML, 'CantidadLineasProduccion'))
            cantidadComponentes = int(inicializacionParametroXML(maquinaActualLexturaXML, 'CantidadComponentes'))
            tiempoEnsamblajeA = int(inicializacionParametroXML(maquinaActualLexturaXML, 'TiempoEnsamblaje'))

            productosActualesMaquinaLectura = maquinaActualLexturaXML.getElementsByTagName('Producto')
            conjuntoProductos = listaProductosXML()

            for productoActualLect in productosActualesMaquinaLectura:
                nombreProducto = inicializacionParametroXML(productoActualLect, 'nombre')
                elaboracion = inicializacionParametroXML(productoActualLect, 'elaboracion')
                conjuntoProductos.insertarProductoXML(nombreProducto, elaboracion)
                
                colaK = ColaElaboracion()
                pasosE = elaboracion.split()
                for paso in pasosE:
                    colaK.insertarCola(paso)  
                segundoActual = 0
                lineasProduccion = ListaLineasProduccion()
                nodoActual = colaK.frente
                while nodoActual:
                    linea, componente = nodoActual.paso.split('C')
                    linea = int(linea[1:])  
                    componente = int(componente)
                    lineasProduccion.insertarLinea(linea)
                    lineasProduccion.insertarComponente(linea, componente, cantidadComponentes, segundoActual)
                    nodoActual = nodoActual.siguiente

                print(f"Producto a ensamblar: {nombreProducto}")
                while not lineasProduccion.recorrerTodasListas():
                    segundoActual += 1
                    lineasProduccion.segundoComponenteT(segundoActual)
                    print(f"Segundo {segundoActual}:")
                    actualLinea = lineasProduccion.primerLinea
                    while actualLinea:
                        print(f"Línea {actualLinea.linea}:")
                        componenteActual = actualLinea.componentes
                        contador = 1
                        while componenteActual:
                            if componenteActual.segundoActual == segundoActual:
                                ensamblar_str = " Ensamblaje" if componenteActual.ensamblar else ""
                                print(f"  Componente {componenteActual.componente}{ensamblar_str}")
                                break
                            componenteActual = componenteActual.siguiente
                            contador += 1
                        actualLinea = actualLinea.siguiente

                tablaC = tablaComponentes(lineasProduccion)
                nodoPr = conjuntoProductos.primerProducto
                while nodoPr:
                    if nodoPr.nombreProducto == nombreProducto:
                        nodoPr.tablaC = tablaC
                        nodoPr.colaK = colaK  
                        break
                    nodoPr = nodoPr.siguienteProducto

            listaGlobalMaquinasLectura.InsertarMaquina(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, conjuntoProductos, colaK, lineasProduccion)

        actualMaquina = listaGlobalMaquinasLectura.primerMaquina
        while actualMaquina:
            print(f"Nombre de maquiina: {actualMaquina.nombreM}")
            print(f"Lineas de produccion: {actualMaquina.cantidadLineas}")
            print(f"Componentes: {actualMaquina.cantidadComponentes}")
            print(f"Tiempo de ensamblaje: {actualMaquina.tiempoEnsamblajeA} segundos")
            print("Lista productos maquina actual:")
            actualProducto = actualMaquina.conjuntoProductos.primerProducto
            while actualProducto:
                print(f"Nombre actual de producto: {actualProducto.nombreProducto}")
                print(" Cola:")
                for paso in actualProducto.elaboracion.split():
                    print(f"{paso}")
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

def tablaComponentes(lineasProduccion):
    tabla = "<table class='min-w-full bg-white'>"
    tabla += "<thead><tr><th class='py-2'>Tiempo</th>"
    
    actualLinea = lineasProduccion.primerLinea
    while actualLinea:
        tabla += f"<th class='py-2'>Línea {actualLinea.linea}</th>"
        actualLinea = actualLinea.siguiente
    tabla += "</tr></thead><tbody>"

    segundoT = 0
    actualLinea = lineasProduccion.primerLinea
    while actualLinea:
        componente = actualLinea.componentes
        while componente:
            if componente.segundoActual > segundoT:
                segundoT = componente.segundoActual
            componente = componente.siguiente
        actualLinea = actualLinea.siguiente

    for segundo in range(1, segundoT + 1):
        tabla += f"<tr class='bg-gray-100'><td class='border px-4 py-2'>{segundo}s</td>"
        actualLinea = lineasProduccion.primerLinea
        while actualLinea:
            componente = actualLinea.componentes
            encontrado = False
            while componente:
                if componente.segundoActual == segundo:
                    tabla += f"<td class='border px-4 py-2'> Se mueve a componente {componente.componente}"
                    if componente.ensamblar:
                        tabla += " - Ensamblado componente"
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

def generarXMLProductos():
    doc = minidom.Document()
    root = doc.createElement('Productos')
    doc.appendChild(root)

    actualMaquina = listaGlobalMaquinasLectura.primerMaquina
    while actualMaquina:
        print(f"Procesando máquina: {actualMaquina.nombreM}")  
        actualProducto = actualMaquina.conjuntoProductos.primerProducto
        while actualProducto:
            print(f"Procesando producto: {actualProducto.nombreProducto}") 
            producto_element = doc.createElement('Producto')
            
            nombreSalida = doc.createElement('Nombre')
            nombretxt = doc.createTextNode(actualProducto.nombreProducto)
            nombreSalida.appendChild(nombretxt)
            producto_element.appendChild(nombreSalida)
            
            elaboracionSalida = doc.createElement('Elaboracion')
            elaboraciontxt = doc.createTextNode(actualProducto.elaboracion)
            elaboracionSalida.appendChild(elaboraciontxt)
            producto_element.appendChild(elaboracionSalida)
            
            root.appendChild(producto_element)
            actualProducto = actualProducto.siguienteProducto
        actualMaquina = actualMaquina.siguienteMaquina

    return doc.toprettyxml(indent="  ")

if __name__ == '__main__':
    slc = 0
    listaDoble = ListaEnlazadaDoble()
    app.run(debug=True)