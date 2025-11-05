from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

# ---- Tải biến môi trường (.env) ----
load_dotenv()

# ---- Cấu hình Flask ----
app = Flask(__name__)

# ---- Cấu hình Cloudinary ----
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Kiểm tra log để chắc chắn biến môi trường đã đọc được
print("✅ Cloudinary config loaded:", os.getenv("CLOUDINARY_CLOUD_NAME"))

# ---- Trang chủ hiển thị gallery ----
@app.route("/")
def gallery():
    # Danh sách ảnh mẫu hoặc từ Cloudinary
    image_urls = [
        "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    ]
    return render_template("gallery.html", images=image_urls)

# ---- Upload ảnh mới ----
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Không có file nào được tải lên", 400

    file = request.files["file"]
    if file.filename == "":
        return "Chưa chọn file", 400

    # Upload lên Cloudinary
    upload_result = cloudinary.uploader.upload(file)
    print("📤 Upload thành công:", upload_result["secure_url"])

    return redirect(url_for("gallery"))

# ---- Chạy app ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
