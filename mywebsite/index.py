from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sqlite3

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/veterinaria.db'

# db = SQLAlchemy(app)

def get_db_connection():
    conn = sqlite3.connect('mywebsite/instance/database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/home") #decorador
def index():
    return render_template("index.html")

@app.route("/", methods=['GET', 'POST']) #decorador
def login():
    metodo = request.method
    if(metodo == 'GET'):
        return render_template("login.html")
    elif (metodo == 'POST'):
        #coneccion 
        conn = get_db_connection();
        #login de ingreso

        #captura de datos
        rut = request.form['rut']
        pass_ = request.form['pass']

        if not rut:
            error = 'El rut es requerido.'
        elif not pass_:
            error = 'La contraseña es requerida'
        else:
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
                flash(error)

        return render_template("index.html")
    else:
        #404
        return render_template("404.html")





@app.route("/register") #decorador
def register():
    return render_template("register.html")

@app.route("/pet") #decorador
def pet():
    return render_template("register_pet.html")

@app.route("/news") #decorador
def news():
    return render_template("news.html")

@app.route("/about") #decorador
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) #para que se autorefresque
