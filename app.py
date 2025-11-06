from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary (API thật của bạn)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4",
    secure=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Không có file nào được chọn'}), 400
    try:
        # ⚙️ Cho phép Cloudinary tự nhận diện ảnh hoặc video
        result = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify({
            'url': result['secure_url'],
            'public_id': result['public_id']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    try:
        # 🔍 Lấy cả ảnh và video
        images = cloudinary.api.resources(type="upload", resource_type="image", max_results=100)
        videos = cloudinary.api.resources(type="upload", resource_type="video", max_results=100)
        files = images.get('resources', []) + videos.get('resources', [])
        files.sort(key=lambda x: x['created_at'], reverse=True)
        return render_template('gallery.html', files=files)
    except Exception as e:
        return f"<h3 style='color:red;'>❌ Lỗi tải dữ liệu: {str(e)}</h3>"

@app.route('/delete/<public_id>', methods=['DELETE'])
def delete_file(public_id):
    try:
        # Xóa ảnh hoặc video tự động
        result = cloudinary.uploader.destroy(public_id, resource_type="auto")
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
