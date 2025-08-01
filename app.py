from flask import Flask, request, render_template, make_response, jsonify
from utils.generate_pdf import generar_ticket

app = Flask(__name__)

# 1) Ruta principal que carga home.html
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# 2) Ruta para el formulario si lo necesitas
@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')

# 3) Endpoint que recibe los datos y devuelve el PDF
@app.route('/tickets', methods=['POST'])
def crear_ticket():
    # Puede venir JSON o campos de formulario
    datos = request.get_json() or request.form.to_dict()
    try:
        pdf_bytes = generar_ticket(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Enviar el PDF como descarga
    response = make_response(pdf_bytes)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set(
        'Content-Disposition',
        'attachment; filename="ticket.pdf"'
    )
    return response

if __name__ == '__main__':
    # Solo en local; Render ignora este bloque
    app.run(host='0.0.0.0', port=5000, debug=True)
