#./app/app.py
from flask import Flask, render_template, session, request, redirect, url_for, flash    
from model import *


app = Flask(__name__)
app.secret_key = 'supersecretkey'


iniciar_prueba_BD()

@app.route('/')
def index():
    return render_template('index.html', matriz=mostrar_movies())

@app.route('/insert-movie', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        id = insert_movie([request.form['title'], request.form['length'], request.form['category'], request.form['rating']])
        flash("Añadida correctamente")
        return redirect(url_for('index'))
    return render_template('insert-movie.html')

@app.route('/delete-movie/<string:id>')
def delete(id):
    borrar_movie(id)
    flash("Borrado correcto")
    return redirect(url_for('index'))
    
@app.route('/edit-movie/<string:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        edit_movie(id, request.form['campo'], request.form['valor'])
        flash("Editada correctamente")
        return(redirect(url_for('index')))
    return render_template('edit-movie.html', id=id)
    

@app.route('/find', methods=['POST'])
def find():
    query = request.form['query']
    response = encontrar_movies(query)
    return render_template('index.html', matriz=response)

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

@app.route('/list-users')
def list():
    return render_template('list-users.html', Users=list_users())
   
