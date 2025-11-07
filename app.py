from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# --- Cấu hình Cloudinary ---
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

DELETE_PASSWORD = "xoa"  # mật khẩu xóa file

# --- Trang chính (upload) ---
@app.route("/")
def index():
    return render_template("index.html")


# --- Xử lý upload ---
@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"success": False, "message": "Không có file nào được chọn!"}), 400

    uploaded_files = []
    for file in files:
        if file and file.filename:
            try:
                result = cloudinary.uploader.upload(file, resource_type="auto")
                uploaded_files.append(result)
            except Exception as e:
                print("❌ Upload lỗi:", e)

    if not uploaded_files:
        return jsonify({"success": False, "message": "Upload thất bại!"}), 500

    print("✅ Đã upload:", [f["public_id"] for f in uploaded_files])
    return jsonify({"success": True, "count": len(uploaded_files)})


# --- Trang thư viện (ảnh + video) ---
@app.route("/gallery")
def gallery():
    try:
        images = cloudinary.api.resources(type="upload", resource_type="image", max_results=100)["resources"]
    except:
        images = []
l
    try:
        videos = cloudinary.api.resources(type="upload", resource_type="video", max_results=100)["resources"]
    except:
        videos = []

    all_items = images + videos
    all_items.sort(key=lambda x: x["created_at"], reverse=True)

    return render_template("gallery.html", resources=all_items)


# --- Xóa file ---
@app.route("/delete/<public_id>", methods=["POST"])
def delete(public_id):
    data = request.get_json()
    password = data.get("password", "")

    if password != "xoa":  # thay mật khẩu bạn muốn
        return jsonify({"error": "Sai mật khẩu"}), 403

    try:
        cloudinary.uploader.destroy(public_id, resource_type="auto")
        return jsonify({"success": True})
    except Exception as e:
        print("Lỗi xóa:", e)
        return jsonify({"error": "Xóa thất bại"}), 500


# --- Chạy ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
