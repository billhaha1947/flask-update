from flask import Flask, render_template, redirect, url_for
import cloudinary
import cloudinary.api
import cloudinary.uploader

app = Flask(__name__)

# --- ⚙️ CẤU HÌNH CLOUDINARY TRỰC TIẾP ---
cloudinary.config(
    cloud_name="dma3eclgv",       # 🔹 Thay bằng cloud name của bạn
    api_key="118974677734641",            # 🔹 Thay bằng API Key
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",      # 🔹 Thay bằng API Secret
    secure=True
)

# --- 🏠 TRANG CHÍNH ---
@app.route("/")
def index():
    return """
    <h1>📸 Cloudinary Demo</h1>
    <a href='/gallery'>Xem thư viện ảnh & video</a>
    """

# --- 🖼️ TRANG GALLERY (ẢNH + VIDEO) ---
@app.route("/gallery")
def gallery():
    try:
        # Lấy ảnh
        image_resources = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            max_results=50
        )["resources"]

        # Lấy video
        video_resources = cloudinary.api.resources(
            type="upload",
            resource_type="video",
            max_results=20
        )["resources"]

        return render_template("gallery.html",
                               images=image_resources,
                               videos=video_resources)

    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)
