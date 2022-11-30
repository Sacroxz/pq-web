from index import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
  mail = StringField('mail', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mail"})
  password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Iniciar Sesion")

class RutForm(FlaskForm):
  rut = StringField('rut', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Rut"})
  submit = SubmitField("Buscar")
  

class EvaluacionPacienteForm(FlaskForm):
  rut_paciente = StringField('rut_paciente', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Rut"})
  temperatura = StringField('temperatura', validators=[InputRequired()], render_kw={"placeholder": "Temperatura"})
  presion_arterial = StringField('presion_arterial', validators=[InputRequired()], render_kw={"placeholder": "Presion Arterial"})
  frecuencia_cardiaca = StringField('frecuencia_cardiaca', validators=[InputRequired()], render_kw={"placeholder": "Frecuencia Cardiaca"})
  frecuencia_respiratoria = StringField('frecuencia_respiratoria', validators=[InputRequired()], render_kw={"placeholder": "Frecuencia Respiratoria"})
  examen_fisico = TextAreaField('examen_fisico', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Examen Fisico"})
  zona_operacion = TextAreaField('zona_operacion', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Zona Operacion"})
  observacion = TextAreaField('observacion', validators=[Length(min=4, max=200)], render_kw={"placeholder": "Observacion"})
  submit = SubmitField("Guardar")

class EvaluacionPostquirurgicaForm(FlaskForm):
  temperatura = StringField('temperatura', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Temperatura"})
  pulso = StringField('pulso', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Pulso"})
  presion_arterial = StringField('presion_arterial', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Presion Arterial"})
  sangrado = StringField('sangrado', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Sangrado"})
  dolor = SelectField('dolor', choices=["No dolor", "Leve", "Moderado", "Intenso", "Maximo Dolor"], validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Dolor"})
  recuperacion = TextAreaField('recuperacion', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Recuperacion"})
  medicacion = TextAreaField('medicacion', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Medicamentos"})
  alimentacion = TextAreaField('alimentacion', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Alimentacion"})
  observacion = TextAreaField('observacion', validators=[Length(min=4, max=200)], render_kw={"placeholder": "Observacion"})
  submit = SubmitField("Guardar")

class CoordinarTrasladoForm(FlaskForm):
  rut_paciente = StringField('rut_paciente', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Rut"})
  fecha = StringField('fecha', validators=[InputRequired()], render_kw={"placeholder": "Fecha"})
  hora = StringField('hora', validators=[InputRequired()], render_kw={"placeholder": "Hora"})
  patente = StringField('patente', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Patente"})
  tipo = SelectField('tipo', choices=["Particular", "Hospital"], validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Tipo Traslado"})
  rut_conductor = StringField('rut_conductor', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Rut Conductor"})
  direccion = StringField('direccion', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Direccion"})
  submit = SubmitField("Guardar")