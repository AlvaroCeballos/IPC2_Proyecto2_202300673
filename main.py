from ListasEnlazadas.ListaEnlazadaCircular import listaEnlazadaCircular # Importar listaCiruclar
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
from ListasEnlazadas.ListaEnlazadaSimple import ListaEnlazadaSimple # Importar lista simple enlazada
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from xml.dom import minidom
import os
from Carro import Carro
from Maquina import Maquina
from Producto import Producto

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura_123'

Lcarro = []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lecturaXML', methods=['POST'])
def lecturaXML():
    def lecturaXML():
        textoXML = request.data

        try:
            xml = ET.fromstring(textoXML)

            for curso_elem in xml.findall('curso'): # Iterar
                nombreCurso = curso_elem.get('nombre') # Obtener el atributo nombre del nodo curso
                seccionCurso = curso_elem.find('seccion').text # Obtener el texto del nodo seccion
                aulaCurso = curso_elem.find('aula').text

                print("Nombre: ", nombreCurso)
                print("Seccion: ", seccionCurso)
                print("Aula: ", aulaCurso)

        except Exception as e:
            return str(e)

    return "Se leyó correctamente el XML"

@app.route('/Agregar')
def agregar():
    return render_template('form.html')

@app.route('/submit', methods=['POST']) 
def submit():
    idTipoAuto = request.form['idTipoAuto']
    Marca = request.form['Marca']
    Modelo = request.form['Modelo']
    Descripcion = request.form['Descripcion']
    Precio_unitario = request.form['Precio_unitario']
    Cantidad = request.form['Cantidad']
    Imagen = request.form['Imagen']

    carroCreado = Carro(idTipoAuto, Marca, Modelo, Descripcion, Precio_unitario, Cantidad, Imagen)
    Lcarro.append(carroCreado)
    print(carroCreado)

    return redirect(url_for('agregar'))



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
    
