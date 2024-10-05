from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from ListasEnlazadas.listaProductosXML import listaProductosXML
from ListasEnlazadas.listaMaquinasXML import listaMaquinasXML
from ListasEnlazadas.pruebaCola import ColaElaboracion
from ListasEnlazadas.listaLineaProduccion import ListaLineasProduccion
from lecturaXMLprueba import obtenerContextoActualLectura, lecturaXMLActual, listaGlobalMaquinasLectura
import lecturaXMLprueba

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
def listarTabla():
    return render_template('archivosSalida.html', listado=listaGlobalMaquinasLectura)
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

    


    

    