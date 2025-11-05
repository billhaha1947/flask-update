from flask import Flask, render_template, request, jsonify, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# ==========================
# 🔧 CẤU HÌNH CLOUDINARY
# ==========================
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dma3eclgv"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "118974677734641"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "8Dhe37EYtXQVaaPpCsDIRRZSrE4"),
)

# ==========================
# 🔒 MẬT KHẨU ADMIN XOÁ ẢNH
# ==========================
ADMIN_PASSWORD = "loc123"  # đổi thành mật khẩu của bạn

# ==========================
# 🏠 TRANG UPLOAD
# ==========================
@app.route("/")
def index():
    return render_template("index.html")

# ==========================
# 📤 UPLOAD FILE LÊN CLOUDINARY
# ==========================
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Không có file nào được gửi"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Tên file trống"}), 400

    try:
        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify(upload_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 🖼️ TRANG THƯ VIỆN GALLERY
# ==========================
@app.route("/gallery")
def gallery():
    try:
        resources = cloudinary.api.resources(type="upload", max_results=50)
        return render_template("gallery.html", resources=resources["resources"])
    except Exception as e:
        return f"Lỗi tải gallery: {e}"

# ==========================
# 🗑️ XOÁ FILE (CHỈ ADMIN)
# ==========================
@app.route("/api/delete/<public_id>", methods=["POST"])
def delete(public_id):
    try:
        data = request.get_json()
        password = data.get("password")

        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Không có quyền xóa."}), 403

        # ✅ Lấy loại file (image/video)
        info = cloudinary.api.resource(public_id)
        resource_type = info.get("resource_type", "image")

        # ✅ Xoá đúng loại file
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 🔥 CHẠY ỨNG DỤNG
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
