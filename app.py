from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import qrcode
import qrcode.image.styledpil
import qrcode.image.styles.moduledrawers as moduledrawers
import qrcode.image.styles.colormasks as colormasks
import os
import uuid
import csv
import zipfile
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'static/temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_path = None
    zip_path = None

    if request.method == 'POST':
        action = request.form.get('action', 'single')

        if action == 'bulk':
            csv_file = request.files.get('csv_file')
            scale = int(request.form.get('scale', 10))
            dark = request.form.get('dark', 'black')
            light = request.form.get('light', 'white')
            error = request.form.get('error', 'H')
            style = request.form.get('style', 'square')
            filetype = request.form.get('filetype', 'png')

            if not csv_file:
                return "No CSV file uploaded", 400

            zip_id = uuid.uuid4().hex
            zip_filename = f"{UPLOAD_FOLDER}/qr_bulk_{zip_id}.zip"

            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                stream = csv_file.stream.read().decode("utf-8").splitlines()
                reader = csv.reader(stream)
                for idx, row in enumerate(reader):
                    if not row:
                        continue
                    qr_data = row[0]
                    qr = qrcode.QRCode(
                        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error.upper()}'),
                        box_size=scale,
                        border=4
                    )
                    qr.add_data(qr_data)
                    qr.make(fit=True)

                    drawer = moduledrawers.RoundedModuleDrawer() if style == 'rounded' else moduledrawers.SquareModuleDrawer()
                    color_mask = colormasks.SolidFillColorMask(back_color=light, front_color=dark)

                    img = qr.make_image(
                        image_factory=qrcode.image.styledpil.StyledPilImage,
                        module_drawer=drawer,
                        color_mask=color_mask
                    ).convert('RGBA')

                    filename = f"qr_{idx+1}.{filetype}"
                    img_bytes = BytesIO()
                    img.save(img_bytes, format=filetype.upper())
                    img_bytes.seek(0)
                    zipf.writestr(filename, img_bytes.read())

            return send_file(zip_filename, as_attachment=True)

        else:
            # SINGLE QR CODE GENERATION (same as earlier)
            data_type = request.form.get('data_type', 'url')
            if data_type == 'url':
                qr_data = request.form['data']
            elif data_type == 'vcard':
                name = request.form['vcard_name']
                phone = request.form['vcard_phone']
                email = request.form['vcard_email']
                company = request.form['vcard_company']
                qr_data = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nFN:{name}\nORG:{company}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
            elif data_type == 'wifi':
                ssid = request.form['wifi_ssid']
                pwd = request.form['wifi_password']
                sec = request.form['wifi_security']
                qr_data = f"WIFI:T:{sec};S:{ssid};P:{pwd};;"
            elif data_type == 'email':
                addr = request.form['email_addr']
                subject = request.form['email_subject']
                body = request.form['email_body']
                qr_data = f"mailto:{addr}?subject={subject}&body={body}"
            elif data_type == 'sms':
                phone = request.form['sms_phone']
                body = request.form['sms_body']
                qr_data = f"sms:{phone}?body={body}"
            elif data_type == 'phone':
                phone = request.form['phone_num']
                qr_data = f"tel:{phone}"
            else:
                qr_data = request.form['data']

            scale = int(request.form.get('scale', 10))
            dark = request.form.get('dark', 'black')
            light = request.form.get('light', 'white')
            error = request.form.get('error', 'H')
            style = request.form.get('style', 'square')
            logo_file = request.files.get('logo')
            filetype = request.form.get('filetype', 'png')

            unique_id = uuid.uuid4().hex
            filename = f"{UPLOAD_FOLDER}/qr_{unique_id}.{filetype}"

            try:
                qr = qrcode.QRCode(
                    error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{error.upper()}'),
                    box_size=scale,
                    border=4
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                drawer = moduledrawers.RoundedModuleDrawer() if style == 'rounded' else moduledrawers.SquareModuleDrawer()
                color_mask = colormasks.SolidFillColorMask(back_color=light, front_color=dark)

                img = qr.make_image(
                    image_factory=qrcode.image.styledpil.StyledPilImage,
                    module_drawer=drawer,
                    color_mask=color_mask
                ).convert('RGBA')

                if logo_file and filetype in ['png', 'jpg', 'jpeg', 'bmp']:
                    logo = Image.open(logo_file)
                    logo_size = int(img.size[0] * 0.2)
                    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
                    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                    img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

                img.save(filename)
                qr_path = filename

            except Exception as e:
                return f"Error: {e}", 500

    return render_template('index.html', qr_path=qr_path)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/bulk', methods=['GET', 'POST'])
def bulk():
    return render_template('bulk.html')

if __name__ == '__main__':
    app.run(debug=True)
