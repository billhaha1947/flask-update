from flask import Flask, render_template, request, redirect, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary trực tiếp trong code (không cần .env)
cloudinary.config(
    cloud_name="dma3eclgv",     # 🔹 Thay bằng tên cloud của bạn
    api_key="118974677734641",           # 🔹 Thay bằng API Key của bạn
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",     # 🔹 Thay bằng API Secret của bạn
    secure=True
)

# 🔐 Mật khẩu để xóa ảnh
DELETE_PASSWORD = "xoa"  # 👉 sửa thành mật khẩu riêng của bạn


# 🏠 Trang upload
@app.route("/")
def index():
    return render_template("index.html")


# 📤 Upload ảnh hoặc video
@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    for file in files:
        cloudinary.uploader.upload(file, resource_type="auto")
    return redirect("/gallery")


# 🖼️ Hiển thị gallery ảnh & video
@app.route("/gallery")
def gallery():
    try:
        # Lấy danh sách file upload từ Cloudinary
        result = cloudinary.api.resources(type="upload", max_results=100)
        resources = result.get("resources", [])
        return render_template("gallery.html", resources=resources)
    except Exception as e:
        return f"Lỗi khi tải thư viện: {e}", 500


# ❌ Xóa ảnh (có yêu cầu mật khẩu)
@app.route("/delete/<public_id>", methods=["POST"])
def delete(public_id):
    password = request.form.get("password")
    if password != DELETE_PASSWORD:
        return jsonify({"success": False, "message": "Sai mật khẩu!"}), 403

    try:
        cloudinary.api.delete_resources([public_id])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
