from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os

app = Flask(__name__)

# 📂 Thư mục lưu file
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 🏠 Trang chính: chỉ để upload file
@app.route('/')
def home():
    html = '''
    <html>
    <head>
        <meta charset="utf-8">
        <title>Upload File</title>
        <style>
            body { font-family: sans-serif; text-align: center; background: #1e1e1e; color: white; }
            input { margin: 10px; }
            a { color: #4CAF50; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>📤 Upload File</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,video/*">
            <br>
            <input type="submit" value="Tải lên">
        </form>
        <p>👉 Xem thư viện file tại <a href="/gallery">/gallery</a></p>
    </body>
    </html>
    '''
    return html


# 📤 API xử lý upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file trong request!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Chưa chọn file!'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'message': 'Upload thành công!', 'filename': file.filename})


# 🖼️ Trang /gallery — hiển thị ảnh và video đã upload
@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    html = '''
    <html>
    <head>
        <meta charset="utf-8">
        <title>Thư viện ảnh & video</title>
        <style>
            body { font-family: sans-serif; background: #111; color: white; text-align: center; }
            .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px; }
            .item { background: #222; padding: 10px; border-radius: 10px; }
            img, video { max-width: 200px; border-radius: 8px; }
            a { color: #4CAF50; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📁 Thư viện file đã upload</h1>
        <p><a href="/">⬅️ Quay lại trang upload</a></p>
        <div class="container">
            {% for f in files %}
                <div class="item">
                    {% if f.endswith('.mp4') or f.endswith('.mov') or f.endswith('.webm') %}
                        <video src="/uploads/{{f}}" controls></video>
                    {% else %}
                        <img src="/uploads/{{f}}" alt="{{f}}">
                    {% endif %}
                    <div>{{f}}</div>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, files=files)


# 🔗 Cho phép truy cập trực tiếp file
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 🚀 Chạy server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
