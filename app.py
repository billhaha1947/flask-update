from flask import Flask, render_template, request, redirect, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- Cấu hình Cloudinary ---
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

DELETE_PASSWORD = "xoa"  # mật khẩu xóa

@app.route("/")
def index():
    return render_template("index.html")

# --- Route upload ---
@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return "Không có file nào được chọn!", 400

    files = request.files.getlist('files[]')
    uploaded_files = []

    for file in files:
        if file:
            # Cloudinary tự nhận dạng ảnh hay video
            upload_result = cloudinary.uploader.upload(
                file,
                resource_type="auto"
            )
            uploaded_files.append(upload_result)

    print("Đã upload:", uploaded_files)
    # ✅ Đừng redirect ở đây — chỉ trả JSON để JS xử lý
    return jsonify({"success": True, "count": len(uploaded_files)})
# --- Route xem gallery ---
@app.route("/gallery")
def gallery():
    # Lấy cả ảnh và video từ Cloudinary
    image_resources = cloudinary.api.resources(type="upload", resource_type="image", max_results=100)["resources"]
    video_resources = cloudinary.api.resources(type="upload", resource_type="video", max_results=100)["resources"]

    # Gộp và sắp xếp
    all_resources = image_resources + video_resources
    all_resources.sort(key=lambda x: x["created_at"], reverse=True)
    return render_template("gallery.html", resources=all_resources)

# --- Route xóa ---
@app.route("/delete/<public_id>", methods=["POST"])
def delete_file(public_id):
    password = request.form.get("password")
    if password != DELETE_PASSWORD:
        return jsonify({"success": False, "message": "Sai mật khẩu!"})

    try:
        # Xóa cả ảnh và video
        cloudinary.api.delete_resources([public_id], resource_type="image")
        cloudinary.api.delete_resources([public_id], resource_type="video")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
