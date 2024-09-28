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
import lecturaXMLprueba

app = Flask(__name__)
app.secret_key = 'pruebaClaveSuperSegura'



@app.route('/LeerXML')
def leer():
    return render_template('subirXML.html')

@app.route('/lecturaXML', methods=['POST'])
def lecturaXML():
    try:
        # Obtener el archivo XML desde la solicitud POST
        if 'xmlFile' not in request.files:
            flash("No se encontró el archivo", "error")
            return redirect("LeerXML")
        
        file = request.files['xmlFile']
        
        if file.filename == '':
            flash("No se seleccionó ningún archivo", "error")
            return redirect("LeerXML")
        
        if file and file.filename.endswith('.xml'):
            xmlString = file.read().decode('utf-8')
            
            # Llamar a la función modificada para procesar el XML
            lecturaXMLActual(xmlString)
            
            flash("Se leyó correctamente el XML", "success")
            return redirect("LeerXML")
        else:
            flash("Formato de archivo no soportado", "error")
            return redirect("LeerXML")
    except Exception as e:
        flash(f"Error al procesar el archivo XML: {str(e)}", "error")
        return redirect("LeerXML")
    

@app.route('/borrarDatos', methods=['POST'])
def borrarDatos():
    lecturaXMLprueba.reiniciarListaGlobal()  # Reiniciar la lista
    flash("Datos borrados correctamente", "success")
    return redirect('/')

# @app.route('/Agregar')
# def agregar():
#     return render_template('form.html')

# @app.route('/submit', methods=['POST']) 
# def submit():
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

    



@app.route('/')
def listar():
    return render_template('index.html')

if __name__ == '__main__':
    slc = 0
    listaCircular = listaEnlazadaCircular()
    listaDoble = ListaEnlazadaDoble()
    listaSimple = ListaEnlazadaSimple()
    app.run(debug=True) 


    


    
