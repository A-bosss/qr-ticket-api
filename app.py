from flask import Flask, render_template, request, redirect, flash
import os, uuid
from utils.generate_pdf import generar_ticket
from db import init_db, descontar_boleto

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "unaclavesecreta")
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1) Leer datos del formulario
        nombre   = request.form.get("nombre", "").strip()
        cantidad = int(request.form.get("cantidad", 1))
        ciudad   = request.form.get("ciudad", "").strip()
        email    = request.form.get("email", "").strip()

        # 2) Intentar descontar 'cantidad' boletos
        if not descontar_boleto(cantidad):
            flash(f"No hay suficientes boletos disponibles. Intentaste comprar {cantidad}.")
            return redirect("/")

        # 3) Generar un ticket_id único
        ticket_id = str(uuid.uuid4())

        # 4) Generar el/los ticket(s)
        generar_ticket(
            nombre    = nombre,
            cantidad  = cantidad,
            ciudad    = ciudad,
            email     = email,
            ticket_id = ticket_id
        )

        flash(f"¡Ticket generado! ID: {ticket_id}")
        return redirect("/")

    # GET → mostrar formulario
    return render_template("form.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    # Asegúrate de que exista la carpeta tickets
    os.makedirs("tickets", exist_ok=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
