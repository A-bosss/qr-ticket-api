# utils/generate_pdf.py

import os
import qrcode
from fpdf import FPDF

def generar_ticket(nombre, cantidad, ciudad, email, ticket_id):
    """
    Genera un PDF con los datos del ticket y un código QR,
    guardándolo en tickets/{ticket_id}.pdf
    """
    # 1) Asegúrate de que exista la carpeta 'tickets'
    os.makedirs("tickets", exist_ok=True)

    # 2) Genera el QR como imagen
    qr_text = (
        f"Electric Wave - 2025\n"
        f"Ticket ID: {ticket_id}\n"
        f"Nombre: {nombre}\n"
        f"Cantidad: {cantidad}\n"
        f"Ciudad: {ciudad}"
    )
    qr = qrcode.make(qr_text)
    qr_path = os.path.join("tickets", f"{ticket_id}_qr.png")
    qr.save(qr_path)

    # 3) Prepara el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Electric Wave – 2025", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Ticket ID: {ticket_id}", ln=True)
    pdf.cell(0, 8, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 8, f"Cantidad: {cantidad}", ln=True)
    pdf.cell(0, 8, f"Ciudad: {ciudad}", ln=True)
    if email:
        pdf.cell(0, 8, f"Email: {email}", ln=True)
    pdf.ln(10)

    # 4) Inserta la imagen del QR
    page_width = pdf.w - 2 * pdf.l_margin
    qr_size = 50
    pdf.image(qr_path,
              x=(page_width - qr_size) / 2 + pdf.l_margin,
              w=qr_size)

    # 5) Guarda el PDF final
    pdf_path = os.path.join("tickets", f"{ticket_id}.pdf")
    pdf.output(pdf_path)

    # 6) Elimina el PNG intermedio
    os.remove(qr_path)

