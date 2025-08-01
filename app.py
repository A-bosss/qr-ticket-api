
from flask import Flask, render_template, request, redirect
import os
from utils.generate_pdf import generar_ticket
from db import init_db, descontar_boleto

app = Flask(__name__)
from flask import render_template
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        numero = request.form["numero"]
        ciudad = request.form["ciudad"]
        email = request.form.get("email", "")
        if descontar_boleto():
            generar_ticket(nombre, numero, ciudad, email)
        return redirect("/")
    return render_template("form.html")


@app.route('/home')
def home():
    return render_template('home.html')
if __name__ == "__main__":
    os.makedirs("tickets", exist_ok=True)
    app.run(debug=True)
