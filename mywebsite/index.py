import email
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from middleware import validar_sesion
import sqlite3

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///mywebsite/instance/database.sqlite'
db=SQLAlchemy(app)


#class Task(db.Model):
#    pass

def get_db_connection():
    conn = sqlite3.connect('mywebsite/instance/database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/home", methods=['GET']) #decorador
@validar_sesion
def home():
    return render_template("home.html")

@app.route("/", methods=['GET', 'POST']) #decorador
def login():
    metodo = request.method
    if(metodo == 'GET'):
        return render_template("login.html")
    elif (metodo == 'POST'):
        #coneccion 
        conn = get_db_connection()
        #login de ingreso

        #captura de datos
        rut = request.form['rut']
        pass_ = request.form['pass']

        error = None
        if not rut:
            error = 'El rut es requerido.'
        elif not pass_:
            error = 'La contraseña es requerida'
        
        if error is None:
            user = conn.execute(
                'SELECT * FROM user WHERE rut = ?', (rut,)
            ).fetchone()
            if user is None:
                error = 'Usuario incorrecto'
            elif user["pass"] != pass_:
                error = 'Contraseña incorrecta.'
            if error is None:
                session.clear()
                session["user_id"] = user['id']
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error = error)

        else:
            return render_template('login.html', error = error)
    else:
        #404
        return render_template("404.html")


@app.route("/cerrarsesion")
def cerrar_sesion():
    session.clear();
    return redirect(url_for('login')) 

@app.route("/register") #decorador
@validar_sesion
def register():
    return render_template("register.html")

@app.route("/mascotas", methods=['GET']) #decorador
@validar_sesion
def mascotas():
    #index, vista encargada de mostrar todas las mascotas
    #conexion
    conn = get_db_connection()
    mascotas = conn.execute('SELECT * FROM animal').fetchall();
    return render_template("mascotas.html", items = mascotas)

@app.route("/mascotas/crear", methods=['GET', 'POST']) #decorador
@validar_sesion
def mascotas_crear():
    metodo = request.method
    if(metodo == 'GET'):
        #Mostramos el formulario
        return render_template("mascotas_crear.html")
    elif (metodo == 'POST'):
        #Ingresamos los datos
        #falta agregar los mensajes flash
        #captura de datos dueño
        cli_nombre= request.form['inputNombre']
        appellido= request.form['inputApellido']
        email= request.form['inputEmail']
        direccion= request.form['inputAddress']
        telefono= request.form['inputTelefono']

        #captura de datos mascota
        mas_nombre= request.form['inputNombreMascota']
        tipo_macota= request.form['inputTipoMascota']
        raza= request.form['inputRaza']
        edad= request.form['inputEdad']
        chip= request.form['inputChip']

        db.session.add(cli_nombre, appellido, email, direccion, telefono, mas_nombre, tipo_macota, raza, edad)


        return render_template("mascotas.html")
    else:
        return render_template("404.html")



@app.route("/news") #decorador
@validar_sesion
def news():
    return render_template("news.html")

@app.route("/about") #decorador
@validar_sesion
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True) #para que se autorefresque
