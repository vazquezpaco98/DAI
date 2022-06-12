#./app/app.py
from flask import Flask, render_template, session, request, redirect, url_for, flash    
from model import *
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


app = Flask(__name__)
app.secret_key = 'supersecretkey'

GoogleMaps(app, key='AIzaSyASB6G9PIQnQ3wZkXJVRVXBhaJ4C1Ycqz4')

iniciar_prueba_BD()

@app.route('/')
def index():
    return render_template('index.html', matriz=mostrar_movies())


#PARTE DE LA PRACTICA 10. FUNCION MAPVIEW PARA VER LA LISTA DE VIDEOCLUBS EN EL MAPA.
@app.route('/mapview', methods=['GET'])
def mapview():
    #sintaxis de marcadores: cuatro campos: 'icon' el color, lat y lng se entienden y 'infobox' es un mensaje que se puede leer al colocarse sobre el marcador.
    marcador1 = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': 33.350,
        'lng' : 45.6,
        'infobox' : "<b>Videoclub original </b>"
    }
    marcador2 = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/bluedot-dot.png',
        'lat': 33.350,
        'lng' : 45.6,
        'infobox' : "<b>Videoclub nuevo de calle Serrano </b>"
    }
    marcadores=[marcador1, marcador2]
    mymap = Map(
        identifier="vista-total",
        lat=33.345,
        lng=45.675,
        markers = marcadores 
    )
    return render_template('mapview.html', mymap=mymap)


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
   
if __name__ == "__main__":
    app.run(debug=True)