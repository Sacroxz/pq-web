from flask import Flask, render_template

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/burger")
def burger():
    return "<p>hola soy un boton<p>"

@app.route("/prueba")
def prueba():
    return render_template("prueba.html")

@app.route("/prueba2")
def prueba2():
    return render_template("prueba2.html")
    
@app.route("/prueba3")
def prueba3():
    return render_template("prueba3.html")