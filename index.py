import os
import sys
import oracledb
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user, UserMixin

oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

app = Flask(__name__)

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DSN = os.environ.get('DB_DSN')

app.config['SQLALCHEMY_DATABASE_URI'] = f'oracle://{DB_USER}:{DB_PASSWORD}@{DB_DSN}/?config_dir=opt/config&wallet_location=opt/config&wallet_password={DB_PASSWORD}'
app.config['SECRET_KEY'] = 'thisisascretkey'
db = SQLAlchemy(app)

class Usuario(db.Model, UserMixin):
  def __init__(self, mail, contrasena):
    self.mail = mail
    self.contrasena = contrasena

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  rut = db.Column(db.String(20), unique=True, nullable=False)
  nombre = db.Column(db.String(20), nullable=False)
  apellido = db.Column(db.String(20), nullable=False)
  telefono = db.Column(db.String(20), nullable=False)
  mail = db.Column(db.String(100), unique=True, nullable=False)
  contrasena = db.Column(db.String(100), nullable=False)
  cargo = db.Column(db.String(100), nullable=False)

migrate = Migrate(app, db, command="migrate")
# bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route("/")
def home():
    print('usuarios:', Usuario.query.all())
    return render_template("home.html")

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    import models
    form = models.LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(mail=form.mail.data).first()
        if user:
            if user.mail == form.mail.data and user.contrasena == form.password.data:
                login_user(user)
                session['logged_in'] = True
                session['cargo'] = user.cargo
                return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Iniciar Sesion', 'url': '/login'}]
    return render_template('login.html', links=links, form=form)

@app.route('/perfil', methods=['GET'])
@login_required
def perfil():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Mi Perfil', 'url': '/perfil'}]
    return render_template('perfil.html', data=current_user, links=links)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    session['cargo'] = None
    return redirect(url_for('home'))

@app.route("/prueba2")
def prueba():
	return render_template("prueba2.html")

# TODO: Implementar rutas para los formularios

if __name__ == '__main__':
    app.run()
    db.create_all()