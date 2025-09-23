from django.shortcuts import render
from django.http import FileResponse
import os, qrcode

from datetime import datetime

def index(request):
    qr_filename = None
    user_link = None

    if request.method == "POST":
        user_link = request.POST.get("userinput")   # ✅ Django way
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

            qr_filename = filename
    return render(request, 'index.html', {
        'qr_filename': qr_filename,
        'user_link': user_link
    })

def download(request, filename):
    filepath = os.path.join("static", filename)
    return FileResponse(open(filepath, 'rb'), as_attachment=True)
