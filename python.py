from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '🟢 Server upload đang chạy!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file trong request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Chưa chọn file'}), 400

    # Lưu file vào thư mục uploads/
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({'message': 'Upload thành công!', 'filename': file.filename})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
