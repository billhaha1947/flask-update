from flask import Flask, request, jsonify, render_template
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Không có file nào được gửi"}), 400
        file = request.files['file']
        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify({"url": upload_result["secure_url"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/api/gallery')
def api_gallery():
    try:
        resources = cloudinary.api.resources(type="upload", max_results=30)
        return jsonify({"items": resources["resources"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete/<public_id>', methods=['DELETE'])
def delete(public_id):
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type="auto")
        return jsonify({"message": "Đã xóa thành công!", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
