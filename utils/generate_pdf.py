import os
from fpdf import FPDF


def generar_ticket(datos: dict) -> bytes:
    pdf = FPDF()
    # Registro de fuentes Unicode
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    font_dir = os.path.join(base_dir, 'fonts')
    pdf.add_font('DejaVu', '',    os.path.join(font_dir, 'DejaVuSans.ttf'),      uni=True)
    pdf.add_font('DejaVu', 'B',   os.path.join(font_dir, 'DejaVuSans-Bold.ttf'), uni=True)

    # Generación del PDF
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, "Electric Wave – 2025", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font('DejaVu', '', 12)
    descripcion = datos.get('descripcion', 'Detalle del ticket')
    pdf.multi_cell(0, 8, descripcion)

    return pdf.output(dest='S').encode('latin-1', 'replace')
