from index import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class LoginForm(FlaskForm):
  mail = StringField('mail', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mail"})
  password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Login")

# class Usuario(db.Model, UserMixin):
#   def __init__(self, rut, nombre, apellido, telefono, mail, contrasena):
#     self.rut = rut
#     self.nombre = nombre
#     self.apellido = apellido
#     self.telefono = telefono
#     self.mail = mail
#     self.contrasena = contrasena

#   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#   rut = db.Column(db.String(20), unique=True, nullable=False)
#   nombre = db.Column(db.String(20), nullable=False)
#   apellido = db.Column(db.String(20), nullable=False)
#   telefono = db.Column(db.String(20), nullable=False)
#   mail = db.Column(db.String(100), unique=True, nullable=False)
#   contrasena = db.Column(db.String(100), nullable=False)