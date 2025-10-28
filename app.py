from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXT = {'png','jpg','jpeg','webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'change_this_to_a_random_value'  # ganti jika production

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<name>')
def uploaded_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Tidak ada file')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Pilih file dulu')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        result = analisa_snr_placeholder(path)
        return render_template('result.html', filename=filename, result=result)
    else:
        flash('Format file tidak diizinkan')
        return redirect(url_for('index'))

def analisa_snr_placeholder(image_path):
    """
    Placeholder sederhana:
    - convert ke grayscale
    - ambil rata-rata brightness tiap baris
    - cari local minima sebagai contoh 'level'
    Ganti dengan algoritma SNR permanen yang kamu mau.
    """
    im = Image.open(image_path).convert('L')
    arr = np.array(im)
    row_mean = arr.mean(axis=1)
    peaks = []
    for i in range(1, len(row_mean)-1):
        if row_mean[i] < row_mean[i-1] and row_mean[i] < row_mean[i+1]:
            peaks.append(int(i))
    peaks = peaks[:10]
    return {
        'levels_found': len(peaks),
        'sample_levels': peaks
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
