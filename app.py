from flask import Flask, request, jsonify, render_template
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary
cloudinary.config(
    cloud_name="dma3eclgv",      # 👈 thay bằng CLOUD_NAME của bạn
    api_key="118974677734641",   # 👈 thay bằng API_KEY của bạn
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"  # 👈 thay bằng API_SECRET của bạn
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Không có file trong request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Chưa chọn file"}), 400

    try:
        # 🩵 Upload ảnh hoặc video lên Cloudinary
        result = cloudinary.uploader.upload(file, resource_type="auto")

        return jsonify({
            "url": result['secure_url'],
            "public_id": result['public_id']
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
