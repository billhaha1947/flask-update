from flask import Flask, request, send_file, send_from_directory, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return send_file('index.html')  # Trả về trang upload


@app.route('/gallery')
def gallery():
    return send_file('gallery.html')  # Trả về trang thư viện


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file nào!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tên file trống!'}), 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    return jsonify({'url': f"/uploads/{file.filename}"})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
