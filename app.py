import os
from flask import Flask, render_template, request, send_file
import qrcode
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    user_link = None

    if request.method == "POST":
        user_link = request.form.get("userinput")
        if user_link:
            # ensure static folder exists
            os.makedirs("static", exist_ok=True)
            filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            qr_path = os.path.join("static", filename)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(qr_path)

            qr_filename = filename  # relative path used in template

    return render_template("index.html", qr_filename=qr_filename, user_link=user_link)


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join("static", filename), as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
