from ListasEnlazadas.ListaEnlazadaCircular import listaEnlazadaCircular # Importar listaCiruclar
from ListasEnlazadas.ListaEnlazadaDoble import ListaEnlazadaDoble # Importar Lista doble enlazada
from ListasEnlazadas.ListaEnlazadaSimple import ListaEnlazadaSimple # Importar lista simple enlazada
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify


app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura_123'

Lcarro = []

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/submitL', methods=['POST']) 
def login():
    usuario = request.form['username']
    password = request.form['password']

    if usuario == 'admin' and password == '2233AD':
        print(usuario)
        print(password)
        return redirect(url_for('agregar'))
        
    else:
        flash('Credenciales incorrectas. Intenta de nuevo.')
        return redirect(url_for('index'))


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

@app.route('/listar')
def listar():
    return render_template('listar.html', listado=Lcarro)

if __name__ == '__main__':
    slc = 0
    listaCircular = listaEnlazadaCircular()
    listaDoble = ListaEnlazadaDoble()
    listaSimple = ListaEnlazadaSimple()
    app.run(debug=True) 