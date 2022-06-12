#./app/app.py
from flask import Flask, request, jsonify, render_template
from model import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'



iniciar_prueba_BD()

#Las de PRACTICA 5

@app.route('/api/movies', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        if request.args.get("Title") is None and request.args.get("Length") is None and request.args.get("Category") is None and request.args.get("Rating") is None:
            lista = mostrar_movies()
        else:
            lista = []
            for i in request.args.keys():
                lista = buscar_por_campo(i, request.args[i]) 
        return jsonify(lista)
    if request.method == 'POST':
        data = request.get_json()
        data = [data.get('Title', ''), data.get('Length', ''), data.get('Category', ''), data.get('Rating', '')]
        return str(insert_movie(data))

@app.route('/api/movies/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_2(id):
    if request.method == 'GET':
        try:
            movie = movie_by_id(id)
            return jsonify(movie)
        except:
            return jsonify({'error':'Not found'}), 404
    if request.method == 'PUT':
        data =request.get_json()
        campos = ['Title', 'Length', 'Category', 'Rating']
        for x in campos:
            if data.get(x, '') is not '':
                editar_movie(id, x, data.get(x, ''))
        return jsonify(movie_by_id(id))
    if request.method == 'DELETE':
        try:
            borrar_movie(id)
            return str(id)
        except:
            return "Vaya mierda"




@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


############################################33


@app.route('/')
def index():
    return "Hola"

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
   
