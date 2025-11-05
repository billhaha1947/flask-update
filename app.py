from flask import Flask, render_template, request, redirect, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary
cloudinary.config(
    cloud_name=os.getenv("dma3eclgv"),
    api_key=os.getenv("118974677734641"),
    api_secret=os.getenv("8Dhe37EYtXQVaaPpCsDIRRZSrE4"),
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "No file", 400
    upload_result = cloudinary.uploader.upload(file)
    return redirect("/gallery")

@app.route("/gallery")
def gallery():
    try:
        result = cloudinary.api.resources(
            type="upload",
            prefix="",   # có thể thêm thư mục nếu cần
            max_results=100
        )
        resources = result.get("resources", [])
        return render_template("gallery.html", resources=resources)
    except Exception as e:
        return f"Lỗi tải gallery: {str(e)}", 500

@app.route("/delete/<public_id>", methods=["DELETE"])
def delete(public_id):
    try:
        cloudinary.api.delete_resources([public_id])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
