from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import segno
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
    if request.method == 'POST':
        # Corrected form data retrieval
        data_type = request.form.get['data_type', 'url']
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
        scale = int(request.form['scale'])
        dark = request.form['dark']
        light = request.form['light']
        error = request.form['error']
        logo_file = request.files.get('logo')
        filetype = request.form['filetype']

        unique_id = uuid.uuid4().hex
        filename = f"{UPLOAD_FOLDER}/qr_{unique_id}.{filetype}"

        try:
            qr = segno.make_qr(data, error=error)

            if filetype == 'svg':
                qr.save(filename, scale=scale, dark=dark, light=light)
            else:
                temp_file = f"{UPLOAD_FOLDER}/temp_{unique_id}.png"
                qr.save(temp_file, scale=scale, dark=dark, light=light)

                img = Image.open(temp_file)

                if logo_file and filetype in ['png', 'jpg', 'jpeg', 'bmp']:
                    logo = Image.open(logo_file)
                    logo_size = int(img.size[0] * 0.2)
                    logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
                    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
                    img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

                img.save(filename)
                os.remove(temp_file)

            qr_path = filename
        except Exception as e:
            return f"Error: {e}", 500

    return render_template('index.html', qr_path=qr_path)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/bulk', methods=['GET', 'POST'])
def bulk():
    if request.method == 'POST':
        file = request.files.get('csvfile')
        if not file or not file.filename.endswith('.csv'):
            return "Please upload a valid CSV file.", 400

        # Prepare a folder for bulk QR images
        bulk_folder = os.path.join(UPLOAD_FOLDER, 'bulk')
        os.makedirs(bulk_folder, exist_ok=True)
        qr_files = []

        # Read CSV and generate QR codes
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            data = row.get('data') or row.get('url') or row.get('URL')
            if not data:
                continue
            unique_id = uuid.uuid4().hex
            filename = f"{bulk_folder}/qr_{unique_id}.png"
            qr = segno.make_qr(data)
            qr.save(filename, scale=10, dark='black', light='white')
            qr_files.append(filename)

        # Create a ZIP file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for file_path in qr_files:
                zipf.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)

        # Optionally, clean up generated files
        for file_path in qr_files:
            os.remove(file_path)

        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='bulk_qrcodes.zip'
        )

    # GET request: Show upload form
    return render_template('bulk.html')

if __name__ == '__main__':
    app.run(debug=True)
