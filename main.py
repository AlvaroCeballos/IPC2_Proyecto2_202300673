from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
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
def Menu():
    print('--------------- Menu Principal ---------------')
    print('1. Cargar archivo XML')
    print('2. Procesar archivo')
    print('3. Escribir archivo de salida XML')
    print('4. Mostrar datos del estudiante')
    print('5. Generar gráfica')
    print('6. Salir')
    print(' ----------------------------------------------')

    slc= int(input('Elija una opción: '))
    return slc

app = Flask(__name__)
app.secret_key = 'pruebaClaveSuperSegura'



@app.route('/LeerXML')
def leer():
    return render_template('subirXML.html')

@app.route('/lecturaXML', methods=['POST'])
def lecturaXML():
    try:

        if 'xmlFile' not in request.files:
            flash("No se encontró el archivo XML", "error")
            return redirect("LeerXML")
        
        file = request.files['xmlFile']
        
        if file.filename == '':
            flash("Por favor seleccionar un archivo XML", "error")
            return redirect("LeerXML")
        
        if file and file.filename.endswith('.xml'):
            xmlString = file.read().decode('utf-8')
            

            lecturaXMLActual(xmlString)
            
            flash("Archivo XML leido correctamente", "success")
            return redirect("LeerXML")
        else:
            flash("Por favor elegir un archivo tipo XML", "error")
            return redirect("LeerXML")
    except Exception as e:
        flash(f"Error al procesar el archivo XML: {str(e)}", "error")
        return redirect("LeerXML")
#---------------------------------------------------------------------------------
@app.route('/salidaArchivosht')
def salida():
    return render_template('archivosSalida.html')

@app.route('/archivosSalida', methods=['POST'])
def archivosSalida():
    try:

        if 'xmlFile' not in request.files:
            flash("No se encontró el archivo XML", "error")
            return redirect("salidaArchivosht")
        
        file = request.files['xmlFile']
        
        if file.filename == '':
            flash("Por favor seleccionar un archivo XML", "error")
            return redirect("salidaArchivosht")
        
        if file and file.filename.endswith('.xml'):
            xmlString = file.read().decode('utf-8')
            

            lecturaXMLActual(xmlString)
            
            flash("Archivo XML leido correctamente", "success")
            return redirect("salidaArchivosht")
        else:
            flash("Por favor elegir un archivo tipo XML", "error")
            return redirect("salidaArchivosht")
    except Exception as e:
        flash(f"Error al procesar el archivo XML: {str(e)}", "error")
        return redirect("salidaArchivosht")
#---------------------------------------------------------------------------------

@app.route('/borrarDatos', methods=['POST'])
def borrarDatos():
    lecturaXMLprueba.reiniciarListaGlobal()  
    flash("Porgrama inicializado correctamnte", "success")
    return redirect('/')
@app.route('/')
def listar():
    return render_template('index.html')

if __name__ == '__main__':
    slc = 0
    listaDoble = ListaEnlazadaDoble()

    
    app.run(debug=True) 

    


    

    