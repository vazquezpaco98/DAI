from flask import Flask, flash, render_template, redirect, request, url_for, session
from random import randrange
import sys
from model import *


#####Los Routings

app = Flask(__name__)
app.secret_key = 'supersecretkey'

iniciarBD()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if credenciales_correctas(request.form['username'], request.form['password']): 
                if 'username' not in session:
                    nombre = request.form['username']
                    password = request.form['password']
                    session['username'] = nombre
                    session['pass'] = password
                    flash('Enhorabuena, '+ nombre + ', estás dentro, a hackear!!')
                    return redirect(url_for('index'))
                else:
                    error = 'Lo siento, hay alguien logueado, cierra sesion antes de abrir'
        else:
            error = 'Lo siento pero no hay usuarios con esas credenciales'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        flash('Sesión cerrada')
    return redirect(url_for('index'))
    

@app.route('/add-user', methods=['GET', 'POST'])
def add():
    error = None
    if request.method == 'POST':
        if adduser(request.form['username'], request.form['password']):
            flash('Usuario '+request.form['username']+' añadido correctamente')
            return redirect(url_for('index'))
        else:
            error = 'Ya existe alguien con ese usuario'
    else:
        if 'username' not in session:
            flash("Tienes que estar logueado para hacer esto")
            return redirect(url_for('index'))
    return render_template('add-user.html', error=error)

@app.route('/edit-user', methods=['GET', 'POST'])
def edit():
    error = None
    if request.method == 'POST':
        if edituser(request.form['username'], request.form['username2'], request.form['password']):
            flash('Usuario '+request.form['username2']+' añadido correctamente')
            return redirect(url_for('index'))
        else:
            error= 'Nadie en la base de datos con esas credenciales'
    else:
        if 'username' not in session:
            flash("Tienes que estar logueado para hacer esto")
            return redirect(url_for('index'))
    
    return render_template('edit-user.html', error=error)


@app.route('/remove-user', methods=['GET', 'POST'])
def remove():
    error = None
    if request.method == 'POST':
        if removeuser(request.form['username']):
            flash('Usuario '+request.form['username']+' eliminado correctamente')
            return redirect(url_for('index'))
        else:
            error = 'No hay nadie con ese usuario'
    else:
        if 'username' not in session:
            flash("Tienes que estar logueado para hacer esto")
            return redirect(url_for('index'))
    
    return render_template('remove-user.html', error=error)


@app.route('/change-pass', methods=['GET', 'POST'])
def change():
    error = None
    if request.method == 'POST':
        if 'username' in session and session['pass'] == request.form['password']:
            if(request.form['password2'] == request.form['password3']):
                session['pass'] = request.form['password2']
                changepass(request.form['username'], request.form['password2'])
                flash("Contraseña cambiada")
                return redirect(url_for('index'))
            else:
                error = 'Contraseña no coincide con la confirmada'
        else:
            error = 'Contraseña incorrecta'
    else:
        if 'username' not in session:
            flash("Tienes que estar logueado para hacer esto")
            return redirect(url_for('index'))
    return render_template('change-pass.html', error=error)

@app.route('/list-users')
def list():
    return render_template('list-users.html', Users=list_users())
        
@app.after_request
def store_visted_urls(response):
    if 'username' in session:
        if session.get('urls') is None:
            session['urls'] = []    
        session['urls'].append(request.url)
        if(len(session['urls']) > 3):
            session['urls'].pop(0)
        session.modified = True

    
    return response

@app.context_processor
def LastVisited():
    if session.get('urls') is not None:
        last = session['urls']
    else:
        last = []
    return dict(lastUrls = last)

#Ejercicios practica2

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/ordena')
def ordena():
    LONGITUD = 30
    RANGO = 100
    arrayList = []
    for i in range(0, randrange(LONGITUD)):
        arrayList.append(randrange(RANGO))
    ordenado_burbuja = arrayList.copy()
    ordenado_mezcla = arrayList.copy()
    ordenado_insercion = arrayList.copy()


    init = time.time()
    bubbleSort(ordenado_burbuja)
    tiempo_burbuja = time.time() - init


    init = time.time()
    mergeSort(ordenado_mezcla)
    tiempo_mezcla = time.time() - init

    init = time.time()
    insertionSort(ordenado_insercion)
    tiempo_insercion = time.time() - init

    return render_template("ordena.html", original=arrayList, burbuja=ordenado_burbuja, mezcla=ordenado_mezcla, insercion=ordenado_insercion, tiempo_burbuja=tiempo_burbuja, tiempo_mezcla=tiempo_mezcla, tiempo_insercion=tiempo_insercion)

@app.route('/criba')
def criba():
    num = randrange(300)
    return render_template("criba.html",cantidad=len(eratostenes(num)), original=eratostenes(num), num=num)

@app.route('/fibonacci')
def fibo():
    num = randrange(40)
    return render_template("fibonacci.html", posicion=num, resultado=fibonacci(num))

@app.route('/corchetes')
def corchete():
    n = randrange(20)
    list = ["[","]"]
    array = []
    for i in range(n):
        array.append(list[randrange(len(list))])
    return render_template('corchetes.html',lista=array, boolean=corchetes(array))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

