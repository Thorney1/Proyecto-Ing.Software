from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from middleware import validar_sesion
from datetime import date

import sqlite3

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',)
app.config.from_object(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///mywebsite/instance/database.sqlite'
#db=SQLAlchemy(app)


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

@app.route("/home_veterinario", methods=['GET']) #decorador
@validar_sesion
def home_veterinario():
    return render_template("home_veterinario.html")

@app.route("/atenciones", methods=['GET']) #decorador
@validar_sesion
def atenciones():
    conn = get_db_connection()
    mascotas = conn.execute('select * from get_animal_all').fetchall()
    return render_template("atenciones.html", items = mascotas)

@app.route("/atenciones/atender/<id>", methods=['GET', 'POST']) #decorador
@validar_sesion
def atender(id):
    metodo = request.method
    conn = get_db_connection()
    mascota = conn.execute(
        "SELECT * FROM get_animal_all WHERE id = ?", (id,)
    ).fetchone()

    if(metodo == 'GET'):

        if mascota is None:
            return 404
        
        conn.execute(
        "UPDATE animal SET estado_animal_id = 2 WHERE id = ?", (id,)
        )

        conn.commit()

        return render_template('atenciones_atender.html', mascota=mascota)
    elif (metodo == 'POST'):
        rowkeys = request.form.getlist('rowKey[]')
        id_vete = session['user_id']
        for row in rowkeys:
             conn.execute(
            'INSERT INTO diagnostico (animal_id, veterinaria_id, descripcion, medicamento, uuid) VALUES(?,?,?,?,?)', 
            ( 
                id,
                id_vete,
                request.form["detail_{}".format(row)],
                request.form["medicamento_{}".format(row)],
                row
            )
            )

        conn.execute(
        "UPDATE animal SET estado_animal_id = 3 WHERE id = ?", (id,)
        )

        conn.commit()

        return redirect(url_for('atenciones'))
    return 404

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
                redirect_to = "home" if user["tipo_usuario"] == 0 else  "home_veterinario";
                
                session.clear()
                session["user_id"] = user['id']
                return redirect(url_for(redirect_to))
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
    mascotas = conn.execute('select * from get_animal_all').fetchall();
    return render_template("mascotas.html", items = mascotas)

@app.route("/mascotas/crear", methods=['GET', 'POST']) #decorador
@validar_sesion
def mascotas_crear():
    metodo = request.method
    if(metodo == 'GET'):
        #Mostramos el formulario
        return render_template("mascotas_crear.html")
    elif (metodo == 'POST'):
        conn = get_db_connection()
        #Ingresamos los datos

        #conn.execute('INSERT INTO %s (name) VALUES (\'%s\')' % ('test', 'sample'))

        #primero ingresamos los datos del cliente, si el cliente existe, tomamos sus datos, y lo introducimos a la mascota


        rut=request.form['cli_rut']
        cli_nombre= request.form['name']
        appellido= request.form['apellido']
        email= request.form['email']
        direccion= request.form['direccion']
        telefono= request.form['telefono']

        #captura de datos mascota
        mas_nombre= request.form['a_nombre']
        tipo_macota= request.form['tipo']
        raza= request.form['raza']
        edad= request.form['edad']
        chip= request.form['chip']
        descripcion= request.form['descripcion']


        fecha_actual = date.today()

        existe_cliente = conn.execute(
                'SELECT * FROM cliente WHERE cli_rut = ?', (rut,)
            ).fetchone()

        id = 0
        if existe_cliente is None:
            #creamos el cliente y obtenemos su valor

            conn.execute(
            'INSERT INTO cliente (name, apellido, cli_rut, telefono, direccion, email) VALUES(?,?,?,?,?,?)', (cli_nombre, appellido, rut, telefono, email, direccion,)
            )
            conn.commit()
            existe_cliente = conn.execute(
                'SELECT * FROM cliente WHERE cli_rut = ?', (rut,)
            ).fetchone();

            id = int(existe_cliente["id"])

        else:   
            #usamos el id
            id = int(existe_cliente["id"])
            
        #se crea la mascota
        conn.execute(
            'INSERT INTO animal (a_nombre, tipo_animal_id, raza, edad, chip, descripcion, ingreso, cliente_id)  VALUES(?,?,?,?,?,?,?,?)', (mas_nombre, tipo_macota, raza, edad, chip, descripcion, fecha_actual, id)
        )            
        conn.commit()
        conn.close()
        flash('La mascota ha sido ingresada exitosamente.')
        return redirect(url_for('mascotas')) 

    else:
        return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=True) #para que se autorefresque
