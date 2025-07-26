
from flask import Flask, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from PIL import Image
import os, io, zipfile

app = Flask(__name__)
OUTPUT_DIR = "certificates"

@app.route("/generate-certificates", methods=["POST"])
def generate_certificates():
    count = int(request.form.get("count", 0))
    if os.path.exists(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, file))
    else:
        os.makedirs(OUTPUT_DIR)

    for i in range(count):
        name = request.form.get(f"name_{i}")
        location = request.form.get(f"location_{i}")
        photo = request.files.get(f"photo_{i}")

        cert_path = os.path.join(OUTPUT_DIR, f"{name}.pdf")
        c = canvas.Canvas(cert_path, pagesize=A3)
        width, height = A3

        # Draw name and location in center
        c.setFont("Helvetica-Bold", 48)
        c.setFillColorRGB(0, 0, 1)  # Blue
        c.drawCentredString(width/2, height/2 + 100, name)
        c.setFont("Helvetica", 36)
        c.drawCentredString(width/2, height/2 + 40, location)

        # Save photo
        if photo:
            img_path = os.path.join(OUTPUT_DIR, f"{name}_photo.jpg")
            photo.save(img_path)
            c.drawImage(img_path, width/2 - 100, height/2 + 180, width=200, height=200)

        c.showPage()
        c.save()

    # Create ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in os.listdir(OUTPUT_DIR):
            zipf.write(os.path.join(OUTPUT_DIR, file), file)

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name="certificates.zip")

if __name__ == "__main__":
    app.run(debug=True)
