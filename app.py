from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# ⚙️ CẤU HÌNH CLOUDINARY TRỰC TIẾP
cloudinary.config(
    cloud_name="dma3eclgv",      # ← thay bằng cloud name của bạn
    api_key="118974677734641",   # ← thay bằng API key của bạn
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",  # ← thay bằng API secret của bạn
    secure=True
)

ADMIN_PASSWORD = "xoa"  # 🔐 Mật khẩu admin để xóa

# 🏠 TRANG CHÍNH
@app.route("/")
def index():
    return render_template("index.html")

# 📤 UPLOAD FILE
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file:
        return "Không có file nào được chọn!", 400

    upload_result = cloudinary.uploader.upload_large(file, resource_type="auto")
    return redirect(url_for("gallery"))

# 🖼️ GALLERY (ẢNH + VIDEO)
@app.route("/gallery")
def gallery():
    try:
        images = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            max_results=50
        )["resources"]

        videos = cloudinary.api.resources(
            type="upload",
            resource_type="video",
            max_results=20
        )["resources"]

        return render_template("gallery.html", images=images, videos=videos)
    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi: {e}</h3>"

# ❌ XOÁ FILE (CÓ MẬT KHẨU)
@app.route("/delete/<res_type>/<public_id>", methods=["POST"])
def delete(res_type, public_id):
    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        return "<h3 style='color:red;'>Sai mật khẩu!</h3>"

    try:
        cloudinary.api.delete_resources([public_id], resource_type=res_type)
        return redirect(url_for("gallery"))
    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi khi xóa: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)
