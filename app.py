from flask import Flask, render_template, request, redirect, url_for, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# Cấu hình Cloudinary (điền API của bạn vào đây)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

# Mật khẩu admin
ADMIN_PASSWORD = "xoa"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    # Lấy ảnh và video từ Cloudinary
    resources = cloudinary.api.resources(type="upload", max_results=100, resource_type="image")["resources"]
    videos = cloudinary.api.resources(type="upload", max_results=50, resource_type="video")["resources"]
    all_media = resources + videos
    return render_template('gallery.html', media=all_media)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    upload_result = cloudinary.uploader.upload(file)
    return jsonify(upload_result)

@app.route('/delete/<public_id>', methods=['POST'])
def delete(public_id):
    password = request.form.get("password", "")
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Sai mật khẩu!"}), 403
    try:
        cloudinary.api.delete_resources([public_id])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
