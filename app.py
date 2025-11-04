from flask import Flask, request, jsonify, send_from_directory
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary
cloudinary.config(
    cloud_name="dma3eclgv",       # 👈 Thay bằng CLOUD_NAME của bạn
    api_key="118974677734641",    # 👈 Thay bằng API_KEY
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"  # 👈 Thay bằng API_SECRET
)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Không có file trong request"}), 400

    file = request.files['file']
    # ⚡ Cho phép Cloudinary tự nhận dạng ảnh hoặc video
    result = cloudinary.uploader.upload(file, resource_type="auto")
    return jsonify({
        "url": result['secure_url'],
        "public_id": result['public_id']
    })

@app.route('/gallery')
def gallery():
    try:
        # ⚙️ Lấy danh sách tất cả tài nguyên (ảnh + video)
        resources = cloudinary.api.resources(
            resource_type="all",
            max_results=50,
            type="upload"
        )
        items = [r['secure_url'] for r in resources['resources']]

        # 🖼️ Tạo giao diện HTML để hiển thị file
        html = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📸 Thư viện Cloudinary</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f3f3f3;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }
                h2 {
                    background: #4CAF50;
                    color: white;
                    padding: 20px;
                    margin: 0;
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 15px;
                    padding: 20px;
                }
                .item {
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    padding: 10px;
                }
                img, video {
                    width: 100%;
                    border-radius: 10px;
                }
                a.btn {
                    display: inline-block;
                    margin: 15px auto;
                    padding: 10px 20px;
                    background: #4CAF50;
                    color: white;
                    border-radius: 8px;
                    text-decoration: none;
                }
                a.btn:hover {
                    background: #45a049;
                }
            </style>
        </head>
        <body>
            <h2>📁 Thư viện ảnh & video</h2>
            <a href="/" class="btn">⬅ Quay lại Upload</a>
            <div class="grid">
        """

        for url in items:
            if any(ext in url for ext in [".mp4", ".mov", "/video/"]):
                html += f'<div class="item"><video controls src="{url}"></video></div>'
            else:
                html += f'<div class="item"><img src="{url}" alt="file"></div>'

        html += "</div></body></html>"

        return html

    except Exception as e:
        return f"<h3 style='color:red;'>❌ Lỗi lấy dữ liệu: {str(e)}</h3>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
