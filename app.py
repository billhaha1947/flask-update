from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 🔧 Cấu hình Cloudinary (thay bằng của mày)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",
    secure=True
)

ADMIN_PASSWORD = "xoa"  # 🔒 mật khẩu admin xoá

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    resources = cloudinary.api.resources(
        type="upload",
        resource_type="auto",
        max_results=100
    )["resources"]
    return render_template("gallery.html", resources=resources)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    res = cloudinary.uploader.upload(file)
    return jsonify({"url": res["secure_url"], "public_id": res["public_id"]})

@app.route("/delete/<public_id>", methods=["POST"])
def delete(public_id):
    data = request.get_json()
    password = data.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"success": False, "message": "Sai mật khẩu!"})

    try:
        cloudinary.uploader.destroy(public_id, invalidate=True, resource_type="image")
        cloudinary.uploader.destroy(public_id, invalidate=True, resource_type="video")
        return jsonify({"success": True})
    except Exception as e:
        print("❌ Lỗi xóa:", e)
        return jsonify({"success": False, "message": "Lỗi khi xóa!"})
