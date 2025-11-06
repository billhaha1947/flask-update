from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# ⚡ CẤU HÌNH CLOUDINARY (thay thông tin của bạn vào đây)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

# 🔐 MẬT KHẨU ADMIN XOÁ FILE
ADMIN_PASSWORD = "xoaanh"

# 🏠 TRANG UPLOAD
@app.route('/')
def index():
    return render_template('index.html')

# 📤 UPLOAD FILE
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return jsonify({"error": "Không có file"}), 400
    upload_result = cloudinary.uploader.upload(file)
    return jsonify({"url": upload_result['secure_url']})

# 📸 TRANG GALLERY
@app.route('/gallery')
def gallery():
    resources = cloudinary.api.resources(type='upload', max_results=100)
    return render_template('gallery.html', resources=resources['resources'])

# 🗑️ XOÁ FILE (có xác thực mật khẩu)
@app.route('/delete/<public_id>', methods=['DELETE'])
def delete_file(public_id):
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Sai mật khẩu"}), 403
    try:
        cloudinary.uploader.destroy(public_id, invalidate=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
