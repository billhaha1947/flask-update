from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# 🔧 Cấu hình Cloudinary trực tiếp
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYTtXQVaaPpCsDIRRZSrE4",
    secure=True
)

# 🏠 Trang chính (Upload)
@app.route('/')
def index():
    return render_template('index.html')

# 🚀 Xử lý upload
@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        upload_result = cloudinary.uploader.upload(file)
        return redirect(url_for('gallery'))
    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi upload: {e}</h3>"

# 🖼️ Trang thư viện
@app.route('/gallery')
def gallery():
    try:
        images = cloudinary.api.resources(type="upload", resource_type="image", max_results=50)["resources"]
        videos = cloudinary.api.resources(type="upload", resource_type="video", max_results=20)["resources"]
        return render_template('gallery.html', images=images, videos=videos)
    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi gallery: {e}</h3>"

if __name__ == '__main__':
    app.run(debug=True)
