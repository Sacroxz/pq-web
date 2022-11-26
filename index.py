import os
from flask import Flask, render_template, request, redirect, url_for, flash
import oracledb

app = Flask(__name__)
app.secret_key = "super secret key"

connection = oracledb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), dsn=os.environ.get('DB_DSN'), config_dir="opt/config", wallet_location="opt/config", wallet_password=os.environ.get('DB_PASSWORD'), encoding="UTF-8")

@app.route("/")
def home():
    cur = connection.cursor()
    cur.execute("SELECT * FROM PERSONS")
    rows = cur.fetchall()
    return render_template("home.html", rows=rows)

@app.route('/prequirurgico')
def prequirurgico():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Prequirurgica', 'url': '/prequirurgico'}]

    return render_template("prequirurgico.html", links=links)

@app.route("/quirurgico")
def quirurgico():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Quirurgica', 'url': '/quirurgico'}]
    return render_template("quirurgico.html", links=links)

@app.route("/postquirurgico")
def postquirurgico():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'}]
    return render_template("postquirurgico.html", links=links)

@app.route('/login')
def login():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Iniciar Sesion', 'url': '/login'}]
    return render_template('login.html', links=links)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    cur = connection.cursor()
    cur = cur.execute("SELECT * FROM USUARIOS WHERE correo = :email AND contrasena = :password", email=email, password=password)
    user = cur.fetchone()
    # TODO: Autenticar al usuario
    if not user:
        flash('Tu correo o contraseña son incorrectos')
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # TODO: Implementar Logout
    return 'Logout'

if __name__ == '__main__':
    app.run()