from ListasEnlazadas.ListaEnlazadaCircular import listaEnlazadaCircular # Importar listaCiruclar
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
from ListasEnlazadas.ListaEnlazadaSimple import ListaEnlazadaSimple # Importar lista simple enlazada
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
import os


app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura_123'


@app.route('/')
def index():
    return render_template('index.html')





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
    
