from ListasEnlazadas.ListaEnlazadaCircular import listaEnlazadaCircular # Importar listaCiruclar
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
from ListasEnlazadas.ListaEnlazadaSimple import ListaEnlazadaSimple # Importar lista simple enlazada
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from xml.dom import minidom
import os
from xml.dom import minidom
from Maquina import Maquina
from Producto import Producto
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from lecturaXMLprueba import obtenerContextoActualLectura, lecturaXMLActual

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura_123'




@app.route('/lecturaXML', methods=['POST'])  # Cambiar a POST
def lecturaXML():
    try:
        # Obtener el contenido del XML desde la solicitud POST
        xmlString = request.data.decode('utf-8')
        
        # Llamar a la función modificada para procesar el XML
        lecturaXMLActual(xmlString)
        
        return "Se leyó correctamente el XML", 200
    except Exception as e:
        return str(e), 400

    return "Se leyó correctamente el XML"


@app.route('/Agregar')
def agregar():
    return render_template('form.html')

@app.route('/submit', methods=['POST']) 
def submit():
    # idTipoAuto = request.form['idTipoAuto']
    # Marca = request.form['Marca']
    # Modelo = request.form['Modelo']
    # Descripcion = request.form['Descripcion']
    # Precio_unitario = request.form['Precio_unitario']
    # Cantidad = request.form['Cantidad']
    # Imagen = request.form['Imagen']

    # carroCreado = Carro(idTipoAuto, Marca, Modelo, Descripcion, Precio_unitario, Cantidad, Imagen)
    # Lcarro.append(carroCreado)
    # print(carroCreado)


    pass

    



@app.route('/ayuda')
def listar():
    return render_template('index.html')

if __name__ == '__main__':
    slc = 0
    listaCircular = listaEnlazadaCircular()
    listaDoble = ListaEnlazadaDoble()
    listaSimple = ListaEnlazadaSimple()
    app.run(debug=True) 

def CargarArchivo(rutaArchivo):
    if os.path.exists(rutaArchivo):
        print('El archivo se ha cargado correctamente')
        return True
    else:
        print('El archivo no existe')
        return False
    

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
        listaActualMaquinasLectura = listaMaquinasXML()

        for maquinaActualLexturaXML in maquinasLecturaActual:
            nombreM = obtenerContextoActualLectura(maquinaActualLexturaXML, 'NombreMaquina')
            cantidadLineas = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadLineasProduccion'))
            cantidadComponentes = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'CantidadComponentes'))
            tiempoEnsamblajeA = int(obtenerContextoActualLectura(maquinaActualLexturaXML, 'TiempoEnsamblaje'))

            productosActualesMaquinaLectura = maquinaActualLexturaXML.getElementsByTagName('Producto')
            listaconjuntoProductos = listaProductosXML()

            for productoActualLect in productosActualesMaquinaLectura:
                nombreProducto = obtenerContextoActualLectura(productoActualLect, 'nombre')
                elaboracion = obtenerContextoActualLectura(productoActualLect, 'elaboracion')
                listaconjuntoProductos.insertarProductoXML(nombreProducto, elaboracion)

            listaActualMaquinasLectura.InsertarMaquina(nombreM, cantidadLineas, cantidadComponentes, tiempoEnsamblajeA, listaconjuntoProductos)

        actualMaquina = listaActualMaquinasLectura.primerMaquina
        while actualMaquina:
            print(f"Nombre maquina actual: {actualMaquina.nombreM}")
            print(f"Total actual de lineas de produccion: {actualMaquina.cantidadLineas}")
            print(f"Componentes actuales: {actualMaquina.cantidadComponentes}")
            print(f"Tiempo en ensamblar una pieza: {actualMaquina.tiempoEnsamblajeA} segundos")
            print("Lista productos maquina actual:")
            actualProducto = actualMaquina.listaconjuntoProductos.primerProducto
            while actualProducto:
                print(f"Nombre actual de producto: {actualProducto.nombreProducto}")
                print(" Elaboracion proceso:")
                for paso in actualProducto.elaboracion.split():
                    print(f"  - {paso}")
                actualProducto = actualProducto.siguienteProducto
            actualMaquina = actualMaquina.siguienteMaquina

    except Exception as errorActualLectura:
        print(f"Error de lectura XML: {errorActualLectura}")
    
