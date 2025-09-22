from flask import Flask, render_template, request, send_file
import qrcode, os
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    user_link = None

    if request.method == "POST":
        user_link = request.form.get("userinput")

        if user_link:
            # create unique filename inside static/
            qr_filename = f"static/qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

            # generate QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # save file
            os.makedirs("static", exist_ok=True)
            img.save(qr_filename)

    return render_template("index.html", qr_filename=qr_filename, user_link=user_link)

# Route to download the QR file
@app.route("/download/<path:filename>")
def download(filename):
    return send_file("static/" + filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
