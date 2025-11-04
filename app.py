from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name="dma3eclgv",     # 👈 thay bằng CLOUD_NAME
    api_key="118974677734641",          # 👈 thay bằng API_KEY
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"     # 👈 thay bằng API_SECRET
)

@app.route('/')
def home():
    return '''
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Tải lên Cloudinary">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Không có file trong request"}), 400

    file = request.files['file']

    # Upload lên Cloudinary
    result = cloudinary.uploader.upload(file)

    # Trả về link ảnh/video
    return jsonify({
        "url": result['secure_url'],
        "public_id": result['public_id']
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
