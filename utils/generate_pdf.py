
import qrcode
from fpdf import FPDF
import uuid
import os
import sqlite3

def generar_ticket(nombre, numero, ciudad, email):
    ticket_id = str(uuid.uuid4())[:8]
    qr_data = f"{ticket_id} - {nombre} - {numero}"

    qr = qrcode.make(qr_data)
    qr_path = f"tickets/{ticket_id}_qr.png"
    qr.save(qr_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="🎟️ Electric Wave 2025", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=2)
    pdf.cell(200, 10, txt=f"Número: {numero}", ln=3)
    pdf.cell(200, 10, txt=f"Ciudad: {ciudad}", ln=4)
    if email:
        pdf.cell(200, 10, txt=f"Email: {email}", ln=5)
    pdf.image(qr_path, x=70, y=60, w=60)

    pdf_path = f"tickets/{ticket_id}_ticket.pdf"
    pdf.output(pdf_path)
    os.remove(qr_path)

    with sqlite3.connect("tickets.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tickets (id, nombre, numero, ciudad, email) VALUES (?, ?, ?, ?, ?)",
                  (ticket_id, nombre, numero, ciudad, email))
        conn.commit()
