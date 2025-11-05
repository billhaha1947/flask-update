from flask import Flask, request, jsonify, render_template
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# 🔐 Mật khẩu admin (chỉ người biết mới xoá được)
ADMIN_PASSWORD = "loc123"  # ⚠️ đổi lại theo ý bạn

# ☁️ Cloudinary config (điền đúng của bạn)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Không có file nào được gửi."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "File trống."}), 400

        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify({"url": upload_result["secure_url"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')

@app.route('/api/gallery')
def get_gallery():
    try:
        results = cloudinary.Search()\
            .expression("resource_type:image OR resource_type:video")\
            .sort_by("created_at", "desc")\
            .max_results(50)\
            .execute()

        files = []
        for r in results["resources"]:
            files.append({
                "url": r["secure_url"],
                "type": r["resource_type"],
                "public_id": r["public_id"]
            })
        return jsonify(files)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete/<public_id>', methods=['POST'])
def delete(public_id):
    try:
        data = request.get_json()
        password = data.get("password")

        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Không có quyền xóa."}), 403

        result = cloudinary.uploader.destroy(public_id, resource_type="auto")
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
