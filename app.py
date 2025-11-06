from flask import Flask, render_template, request, redirect, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# Cấu hình Cloudinary — thay bằng thông tin của mày
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

DELETE_PASSWORD = "12345"  # mật khẩu xóa

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gallery")
def gallery():
    # Lấy cả ảnh và video từ Cloudinary
    image_resources = cloudinary.api.resources(type="upload", resource_type="image", max_results=100)["resources"]
    video_resources = cloudinary.api.resources(type="upload", resource_type="video", max_results=100)["resources"]

    # Gộp lại chung 1 danh sách
    all_resources = image_resources + video_resources
    # Sắp xếp theo ngày tạo (mới nhất lên đầu)
    all_resources.sort(key=lambda x: x["created_at"], reverse=True)
    return render_template("gallery.html", resources=all_resources)

@app.route("/delete/<public_id>", methods=["POST"])
def delete_file(public_id):
    password = request.form.get("password")
    if password != DELETE_PASSWORD:
        return jsonify({"success": False, "message": "Sai mật khẩu!"})

    # Xóa cả ảnh và video
    try:
        cloudinary.api.delete_resources([public_id], resource_type="image")
        cloudinary.api.delete_resources([public_id], resource_type="video")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
