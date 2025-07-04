from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from BBCdb import BBC, db
from app import create_App
import os
import textwrap


def sports_email_format():
    c = canvas.Canvas("Sports.pdf", pagesize=letter)

    c.setTitle("Sports-By NEWS-Mail")
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)

    news = BBC.query.all()

    x = 50  # horizontal margin
    y = 750  # vertical start position
    line_height = 20

    for i, n in enumerate(news, start=1):
        if y < 50:
            c.showPage()
            c.setFont('Helvetica', 12)
            y = 750

        c.drawString(x, y, f"{i}. {n.title}")
        y -= line_height

        summary_lines = textwrap.wrap(n.summary, width=90)
        for line in summary_lines:
            if y < 50:
                c.showPage()
                c.setFont('Helvetica', 12)
                y = 750
            c.drawString(x + 20, y, line)
            y -= line_height

        y -= 10  # spacing between articles

    c.save()


if __name__ == "__main__":
    app = create_App()
    path = r"C:\Users\jafri\OneDrive\Desktop\Resume Project\NEWS-Mail\NEWS-Mail"
    file = "Sports.pdf"
    final_location = os.path.join(path, file)

    if os.path.exists(final_location):
        os.remove(final_location)

    with app.app_context():
        sports_email_format()
