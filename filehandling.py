from io import BytesIO
from reportlab.pdfgen import canvas
def create_pdf(text):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    textobject = p.beginText(40, 800)
    for line in text.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    p.save()
    buffer.seek(0)
    return buffer
