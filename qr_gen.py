import qrcode

def generare_qr_code(text, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    
# Input text to generate QR code for
text = "https://oladayo-portfolio.vercel.app/"
    
# File name to save QR code image
file_name = "qr_code.png"

# Generate the QR code
generare_qr_code(text, file_name)
print(f"QR code saved as {file_name}")