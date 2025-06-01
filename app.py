from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
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

def generate_qr(data, scale, dark, light, filetype, logo_file=None):
    unique_id = uuid.uuid4().hex
    filename = f"{UPLOAD_FOLDER}/qr_{unique_id}.{filetype}"
    
    qr = segno.make_qr(data)
    
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
    
    return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_path = None
    if request.method == 'POST':
        data_type = request.form.get('data_type', 'url')

        if data_type == 'url':
            qr_data = request.form['data']
        elif data_type == 'vcard':
            qr_data = f"""BEGIN:VCARD
VERSION:3.0
N:{request.form['vcard_name']}
FN:{request.form['vcard_name']}
ORG:{request.form['vcard_company']}
TEL:{request.form['vcard_phone']}
EMAIL:{request.form['vcard_email']}
END:VCARD"""
        elif data_type == 'wifi':
            qr_data = f"WIFI:T:{request.form['wifi_security']};S:{request.form['wifi_ssid']};P:{request.form['wifi_password']};;"
        elif data_type == 'email':
            qr_data = f"mailto:{request.form['email_addr']}?subject={request.form['email_subject']}&body={request.form['email_body']}"
        elif data_type == 'sms':
            qr_data = f"sms:{request.form['sms_phone']}?body={request.form['sms_body']}"
        elif data_type == 'phone':
            qr_data = f"tel:{request.form['phone_num']}"
        else:
            qr_data = request.form['data']

        try:
            scale = int(request.form.get('scale', 10))
            dark = request.form.get('dark', 'black')
            light = request.form.get('light', 'white')
            filetype = request.form.get('filetype', 'png')
            logo_file = request.files.get('logo')

            qr_path = generate_qr(qr_data, scale, dark, light, filetype, logo_file)
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

        bulk_folder = os.path.join(UPLOAD_FOLDER, 'bulk')
        os.makedirs(bulk_folder, exist_ok=True)
        qr_files = []

        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in reader:
            data = row.get('data') or row.get('url') or row.get('URL')
            if not data:
                continue
            filename = generate_qr(data, scale=10, dark='black', light='white', filetype='png')
            qr_files.append(filename)

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for file_path in qr_files:
                zipf.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)

        for file_path in qr_files:
            os.remove(file_path)

        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='bulk_qrcodes.zip')

    return render_template('bulk.html')

if __name__ == '__main__':
    app.run(debug=True)
