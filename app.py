from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.api
import cloudinary.uploader

app = Flask(__name__)

# --- Cấu hình Cloudinary ---
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYTkQVaaPpCsDIRRZSrE4",
    secure=True
)

# --- Mật khẩu admin để xóa ---
ADMIN_PASSWORD = "xoa"  # Đổi tùy ý

# --- Trang index (upload) giữ nguyên ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Trang gallery ---
@app.route("/gallery")
def gallery():
    try:
        # Lấy ảnh và video
        images = cloudinary.api.resources(resource_type="image", max_results=100)["resources"]
        videos = cloudinary.api.resources(resource_type="video", max_results=100)["resources"]
        return render_template("gallery.html", images=images, videos=videos)
    except Exception as e:
        return f"Lỗi khi tải gallery: {str(e)}"

# --- Xóa file (image/video) ---
@app.route("/delete/<path:public_id>", methods=["DELETE", "POST"])
def delete_file(public_id):
    if request.method == "DELETE":
        res_type = request.args.get("type", "image")
        password = request.args.get("password", "")
    else:
        res_type = request.form.get("type", "image")
        password = request.form.get("password", "")

    if password != ADMIN_PASSWORD:
        return jsonify({"ok": False, "message": "Sai mật khẩu!"}), 401

    if res_type not in ("image", "video", "raw"):
        return jsonify({"ok": False, "message": "Loại tài nguyên không hợp lệ."}), 400

    try:
        result = cloudinary.api.delete_resources([public_id], resource_type=res_type)
        return jsonify({"ok": True, "message": "✅ Xóa thành công!", "result": result})
    except Exception as e:
        return jsonify({"ok": False, "message": f"Lỗi khi xóa: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
