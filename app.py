
from flask import Flask
from flask import render_template, request, redirect, url_for, escape
from flask import session
from flask.helpers import flash
from flask_mysqldb import MySQL
from werkzeug.utils import escape
app = Flask(__name__)
app.secret_key = "conytraseña23"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sistemadelogin"

mysql=MySQL(app)


@app.route("/", methods=["GET","POST"])
def login():
    mensaje = None
    if request.method == "POST":
        email = request.form["email"]
        contraseña = request.form["contrasena"]
        try:
            cursor = mysql.connection.cursor()

            cursor.execute(("select email,contrasena from usuarios where email='{0}'and  contrasena='{1}'").format(
                email, contraseña))
            resultado = cursor.fetchone()
            if resultado:
                
                session['email'] = email
                session['contrasena'] = contraseña    
                return redirect(url_for("listar"))
            else:
                mensaje ="Email o clave incorrecta"
        except ValueError:
            pass
    
    return render_template("login.html",ms=mensaje)



@app.route("/listar")
def listar():
    mensaje ="nesesitas logearte"
    if  'email' in session:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM registro")
            resultado = cursor.fetchall()
            return render_template("listar.html", listar=resultado)
        except ValueError:
            pass
        
    
    else:
       return render_template("login.html", ms=mensaje)

@app.route("/mostrar")
def mostar():
    return render_template("registroC.html")


@app.route("/editar/<int:id>")
def editar(id):
    mensaje = "nesesitas logearte"
    if 'email' in session:
        try:
            cursor = mysql.connection.cursor()
            editar = f"SELECT * FROM registro WHERE id={id}"
            cursor.execute(editar)
            registro = cursor.fetchone()
            return render_template("editar.html",ed=registro)

        except Exception as ex:
            print (ex)
    else:
        return render_template("login.html", ms=mensaje)

@app.route("/aRegistro",methods=["POST"])
def AgregarRegistro():
    mensaje="nesesitas logearte"
    if 'email' in session:
        if request.method=="POST":
            nombre = request.form['nombre']
            contacto = request.form['numero']
            profecion=request.form['profecion']
            try:
                cursor=mysql.connection.cursor()
                insertar=f"INSERT INTO registro (nombre,contacto,profecion) VALUES('{nombre}','{contacto}','{profecion}')"
                cursor.execute(insertar)
                mysql.connection.commit()
                return redirect(url_for("listar"))
            except Exception as ex:
                print(ex)
    else:
        return render_template("login.html",ms=mensaje)


@app.route("/eliminar/<int:id>")
def eleminar(id):
    mensaje="nesesitas logearte"
    
    if 'email' in session:
        try:
            cursor = mysql.connection.cursor()
            eliminar= f"DELETE FROM registro WHERE id={id}"
            cursor.execute(eliminar)
            cursor.connection.commit()
            return redirect(url_for("listar"))
        except Exception as ex:
            print(ex)
    else:
        return render_template("login.html", ms=mensaje)


@app.route("/actulizar/<int:id>", methods=["POST"])
def actulizar(id):
    mensaje = "nesesitas logearte"
    if 'email'in session:
        if request.method=="POST":
            nombre = request.form['nombre']
            contacto = request.form['numero']
            profecion = request.form['profecion']
            try:
                cursor = mysql.connection.cursor()
                actulizar = f"UPDATE registro SET nombre='{nombre}', contacto='{contacto}',profecion='{profecion}' WHERE id={id}"
                cursor.execute(actulizar)
                cursor.connection.commit()
                
            except Exception as ex:
                print(ex)
        return redirect(url_for("listar"))
    else:
        return render_template("login.html", ms=mensaje)
    
    
@app.route("/salir")
def salir():
    session.pop('email', None)
    session.pop('contrasena', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
