from flask import Flask, render_template
import cloudinary
import cloudinary.api

app = Flask(__name__)

# ⚡ KHAI BÁO CLOUDINARY TRỰC TIẾP (điền thông tin của bạn vào)
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    try:
        # Lấy danh sách ảnh từ Cloudinary
        resources = cloudinary.api.resources(type="upload", max_results=100)
        images = [r["secure_url"] for r in resources["resources"]]
        return render_template("gallery.html", images=images)
    except Exception as e:
        return f"Lỗi khi tải ảnh: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
