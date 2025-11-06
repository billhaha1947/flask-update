from flask import Flask, render_template, redirect, url_for
import cloudinary
import cloudinary.api
import cloudinary.uploader

app = Flask(__name__)

# 🌩️ CẤU HÌNH CLOUDINARY TRỰC TIẾP (bảo mật + HTTPS)
cloudinary.config(
    cloud_name="dma3e1gv",               # Thay bằng cloud_name của bạn
    api_key="118974677734641",           # Thay bằng api_key của bạn
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",  # Thay bằng api_secret thật
    secure=True                          # ⚡ Bắt buộc để dùng HTTPS
)


# 🏠 TRANG CHÍNH
@app.route("/")
def index():
    return """
        <h1>📸 Cloudinary Demo</h1>
        <a href='/gallery'>Xem thư viện ảnh & video</a>
    """


# 🖼️ TRANG GALLERY (ẢNH + VIDEO)
@app.route("/gallery")
def gallery():
    try:
        # Lấy ảnh
        image_resources = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            max_results=50
        ).get("resources", [])

        # Lấy video
        video_resources = cloudinary.api.resources(
            type="upload",
            resource_type="video",
            max_results=20
        ).get("resources", [])

        return render_template("gallery.html",
                               images=image_resources,
                               videos=video_resources)

    except Exception as e:
        # Hiển thị lỗi để debug
        return f"<h3 style='color:red;'>❌ Lỗi: {e}</h3>"


if __name__ == "__main__":
    app.run(debug=True)
