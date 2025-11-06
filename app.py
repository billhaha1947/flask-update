from flask import Flask, render_template, request, jsonify, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# 🔧 Cấu hình Cloudinary (dùng API của bạn)
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
        result = cloudinary.uploader.upload(file)
        return jsonify({
            'url': result['secure_url'],
            'public_id': result['public_id']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    try:
        res = cloudinary.api.resources(max_results=100, type="upload")
        return render_template('gallery.html', files=res.get('resources', []))
    except Exception as e:
        return f"<h3 style='color:red;'>❌ Lỗi tải dữ liệu: {str(e)}</h3>"

@app.route('/delete/<public_id>', methods=['DELETE'])
def delete_file(public_id):
    try:
        result = cloudinary.uploader.destroy(public_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
