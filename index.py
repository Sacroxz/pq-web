import os
import sys
import oracledb
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user, UserMixin

oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

app = Flask(__name__)

# For Vercel
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

class Traslado(db.Model):
    def __init__(self, id, fecha, hora, patente, tipo, rut_conductor, rut_paciente, direccion):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.patente = patente
        self.rut_conductor = rut_conductor
        self.rut_paciente = rut_paciente
        self.tipo = tipo
        self.direccion = direccion
    
    __tablename__ = 'traslado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(20), nullable=False)
    patente = db.Column(db.String(20), db.ForeignKey('transporte.patente'), nullable=False)
    rut_conductor = db.Column(db.String(20), db.ForeignKey('conductor.rut'), nullable=False)
    rut_paciente = db.Column(db.String(20), db.ForeignKey('paciente.rut'), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
class Transporte(db.Model):
    __tablename__ = 'transporte'
    patente = db.Column(db.String(20), primary_key=True)
    disponible = db.Column(db.Boolean, nullable=False)
    traslado = db.relationship('Traslado', backref='transporte', lazy=True)
class Conductor(db.Model):
    __tablename__ = 'conductor'
    rut = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    traslado = db.relationship('Traslado', backref='conductor', lazy=True)
class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, autoincrement=True)
    rut = db.Column(db.String(20), primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    sexo = db.Column(db.Boolean, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    traslado = db.relationship('Traslado', backref='paciente', lazy=True)
    evaluacion = db.relationship('Evaluacion', backref='paciente', lazy=True)
class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    rut_paciente = db.Column(db.String(20), db.ForeignKey('paciente.rut'), nullable=False)
    temperatura = db.Column(db.Integer, nullable=False)
    presion_arterial = db.Column(db.Integer, nullable=False)
    frecuencia_cardiaca = db.Column(db.Integer, nullable=False)
    frecuencia_respiratoria = db.Column(db.Integer, nullable=False)
    examen_fisico = db.Column(db.String(100), nullable=False)
    zona_operacion = db.Column(db.String(100), nullable=False)
    observacion = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date)

migrate = Migrate(app, db, command="migrate")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route("/")
def home():
    print("HEY")
    # print('usuarios:', Usuario.query.all())
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
                session['user'] = user.nombre
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
    session['user'] = None
    session['cargo'] = None
    return redirect(url_for('home'))

@app.route("/prueba2")
def prueba():
	return render_template("prueba2.html")

@app.route("/postquirurgico/evaluacion_paciente", methods=['GET', 'POST'])
@login_required
def evaluacion_paciente():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Evaluacion Paciente', 'url': '/postquirurgico/evaluacion_paciente'}]
    from models import EvaluacionPacienteForm
    evaluacion_paciente_form = EvaluacionPacienteForm()
    if request.method == 'POST':
        print(evaluacion_paciente_form.validate_on_submit())
    if evaluacion_paciente_form.validate_on_submit():
        paciente = Paciente.query.filter_by(rut=request.form['rut_paciente']).first()
        if paciente:
            evaluacion = Evaluacion(
                rut_paciente=request.form['rut_paciente'],
                temperatura=request.form['temperatura'],
                presion_arterial=request.form['presion_arterial'],
                frecuencia_cardiaca=request.form['frecuencia_cardiaca'],
                frecuencia_respiratoria=request.form['frecuencia_respiratoria'],
                examen_fisico=request.form['examen_fisico'],
                zona_operacion=request.form['zona_operacion'],
                observacion=request.form['observacion']
            )
            db.session.add(evaluacion)
            db.session.commit()
            flash('Evaluacion agregada correctamente')
            return redirect(url_for('postquirurgico'))
        else:
            flash('Paciente no encontrado')
            return redirect(url_for('evaluacion_paciente'))
    return render_template("evaluacion_paciente.html", evaluacion_paciente_form=evaluacion_paciente_form, links=links)

@app.route("/postquirurgico/evaluacion_post_quirurgica")
@login_required
def evaluacion_post_quirurgica():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Evaluacion Post Anestesica', 'url': '/postquirurgico/evaluacion_post_quirurgica'}]
    from models import RutForm, EvaluacionPostquirurgicaForm
    rut_form = RutForm()
    evaluacion_post_quirurgica_form = EvaluacionPostquirurgicaForm()
    return render_template("evaluacion_post_quirurgica.html", 
        rut_form=rut_form, evaluacion_post_quirurgica_form=evaluacion_post_quirurgica_form,
        links=links)

@app.route("/postquirurgico/coordinar_traslado", methods=['GET', 'POST'])
@login_required
def coordinar_traslado():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Coordinar Traslado', 'url': '/postquirurgico/coordinar_traslado'}]
    from models import CoordinarTrasladoForm
    coordinar_traslado_form = CoordinarTrasladoForm()

    print(coordinar_traslado_form.validate_on_submit())
    print(coordinar_traslado_form.data)
    if coordinar_traslado_form.validate_on_submit():
        id = 2
        rut_paciente = request.form['rut_paciente']
        fecha = request.form['fecha']
        hora = request.form['hora']
        patente = request.form['patente']
        tipo = request.form['tipo']
        rut_conductor = request.form['rut_conductor']
        direccion = request.form['direccion']
        
        traslado = Traslado(id=id, fecha=fecha, hora=hora, patente=patente, rut_conductor=rut_conductor, rut_paciente=rut_paciente, tipo=tipo, direccion=direccion)
        db.session.add(traslado)
        db.session.commit()
        db.session.flush()
    return render_template("coordinar_traslado.html", 
        coordinar_traslado_form=coordinar_traslado_form,
        links=links)

@app.route("/postquirurgico/paciente", methods=['GET', 'POST'])
@login_required
def estado_paciente():
    links = [
            {'name': 'Home', 'url': '/'}, 
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Estado Paciente', 'url': '/postquirurgico/paciente'}]
    query = "SELECT * FROM paciente"
    pacientes = db.engine.execute(query)
    return render_template("estado_paciente.html", links=links, pacientes=pacientes)

@app.route("/postquirurgico/paciente/<id>", methods=['GET', 'POST'])
@login_required
def estado_paciente_rut(id):
    links = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Estado Paciente', 'url': '/postquirurgico/estado_paciente/'+id}]
    query = "SELECT * FROM paciente WHERE id = %s" % id
    paciente = db.engine.execute(query)
    for row in paciente:
        pac = row
    query_evaluaciones = "SELECT * FROM evaluacion WHERE rut_paciente = '%s'" % pac.rut
    evaluaciones = db.engine.execute(query_evaluaciones)
    return render_template("datos_paciente.html", pac=pac, evaluaciones = evaluaciones, id=id, links=links)

@app.route("/postquirurgico/paciente/<id>/evaluacion/<id_evaluacion>", methods=['GET', 'POST'])
@login_required
def estado_paciente_rut_evaluacion(id, id_evaluacion):
    links = [
            {'name': 'Home', 'url': '/'},
            {'name': 'Fase Postquirurgica', 'url': '/postquirurgico'},
            {'name': 'Estado Paciente', 'url': '/postquirurgico/paciente/'+id},
            {'name': 'Evaluacion', 'url': '/postquirurgico/paciente/'+id+'/evaluacion/'+id_evaluacion}]

    query_evaluacion = "SELECT * FROM evaluacion WHERE id = %s" % id_evaluacion
    evaluacion = db.engine.execute(query_evaluacion)
    for row in evaluacion:
        eva = row
    return render_template("evaluacion.html", id=id, links=links, eva=eva)

if __name__ == '__main__':
    app.run()
    db.create_all()