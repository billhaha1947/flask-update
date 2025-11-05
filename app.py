from flask import Flask, render_template, request, redirect, url_for, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# ---------- Cấu hình Cloudinary ----------
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

# ---------- Trang Upload ----------
@app.route("/")
def index():
    return render_template("upload.html")

# ---------- Upload ----------
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    upload_result = cloudinary.uploader.upload(file)
    return redirect(url_for("gallery"))

# ---------- Gallery ----------
@app.route("/gallery")
def gallery():
    # Lấy cả ảnh + video
    resources = cloudinary.api.resources(
        type="upload",
        resource_type="all",
        max_results=100
    )
    return render_template("gallery.html", resources=resources["resources"])

# ---------- Xóa file ----------
@app.route("/delete/<public_id>", methods=["DELETE"])
def delete_file(public_id):
    result = cloudinary.uploader.destroy(public_id, resource_type="image")
    if result.get("result") != "ok":
        # thử xoá video nếu không phải ảnh
        result = cloudinary.uploader.destroy(public_id, resource_type="video")
    return jsonify(result)

# ---------- Chạy ----------
if __name__ == "__main__":
    app.run(debug=True)
