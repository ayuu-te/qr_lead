from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import segno
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
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

            return render_template('index.html', qr_path=filename)
        except Exception as e:
            return f"Error: {e}", 500

    return render_template('index.html')

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
