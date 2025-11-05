from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import traceback

app = Flask(__name__)

# ====== Cấu hình Cloudinary từ env hoặc fallback (thay bằng giá trị thật nếu muốn) ======
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dma3eclgv"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "118974677734641"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "8Dhe37EYtXQVaaPpCsDIRRZSrE4"),
)

# Mật khẩu admin (nên đặt qua biến môi trường trên production)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "loc123")

# ====== Trang upload ======
@app.route("/")
def index():
    return render_template("index.html")

# ====== API upload trả JSON ======
@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Không có file gửi lên"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Tên file trống"}), 400

        # upload (resource_type="auto" cho ảnh/video)
        result = cloudinary.uploader.upload(file, resource_type="auto")
        # Trả về toàn bộ result (bạn có thể chỉ trả secure_url)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        # In traceback cho log (terminal / render logs)
        traceback.print_exc()
        return jsonify({"error": "Lỗi server khi upload", "detail": str(e)}), 500

# ====== Trang gallery (server render) ======
@app.route("/gallery")
def gallery():
    try:
        # Lấy tất cả loại resource (image + video + raw...)
        response = cloudinary.api.resources(type="upload", resource_type="all", max_results=200)
        resources = response.get("resources", [])
        return render_template("gallery.html", resources=resources)
    except Exception as e:
        traceback.print_exc()
        return f"<h3>Lỗi tải gallery: {e}</h3>", 500

# ====== API xóa file (POST với password) ======
@app.route("/api/delete/<public_id>", methods=["POST"])
def api_delete(public_id):
    try:
        data = request.get_json() or {}
        password = data.get("password")
        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Không có quyền xóa."}), 403

        # Lấy thông tin file trước (để biết resource_type)
        try:
            info = cloudinary.api.resource(public_id)
            resource_type = info.get("resource_type", "image")
        except cloudinary.api.Error as e:
            # Nếu không tìm thấy bằng resource_type mặc định, thử image/video
            resource_type = "image"

        # Xoá file đúng loại
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Lỗi server khi xóa", "detail": str(e)}), 500

# ====== Route hỗ trợ xóa (cũ / nếu bạn dùng DELETE trực tiếp) ======
@app.route("/delete/<public_id>", methods=["DELETE"])
def delete_short(public_id):
    # Hỗ trợ gọi DELETE (không an toàn) — optional
    try:
        # cố gắng xóa image rồi video
        r = cloudinary.uploader.destroy(public_id, resource_type="image")
        if r.get("result") != "ok":
            r = cloudinary.uploader.destroy(public_id, resource_type="video")
        return jsonify(r)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # debug=True chỉ khi chạy local; trên production để False
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
