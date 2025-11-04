from flask import Flask, request, render_template_string
import cloudinary
import cloudinary.uploader
from cloudinary import Search

app = Flask(__name__)

# 🔧 Cấu hình Cloudinary (thay bằng thông tin thật của bạn)
cloudinary.config(
    cloud_name=""dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

# 🏠 Trang upload chính
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            upload_result = cloudinary.uploader.upload(file)
            return f"""
            <h2>✅ Upload thành công!</h2>
            <p><a href='{upload_result['secure_url']}' target='_blank'>Xem file tại đây</a></p>
            <a href='/gallery'>📸 Xem thư viện</a><br><br>
            <a href='/'>⬅ Quay lại Upload</a>
            """
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>☁ Upload lên Cloudinary</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0; }
            form { background: white; padding: 20px; border-radius: 10px; display: inline-block; }
            input[type=file] { margin: 10px; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
            button:hover { background: #45a049; }
            #progress-container { width: 100%; background: #ddd; border-radius: 5px; display: none; margin-top: 10px; }
            #progress-bar { height: 20px; background: #4CAF50; width: 0%; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h2>☁ Tải ảnh hoặc video lên Cloudinary</h2>
        <form id="uploadForm" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <button type="submit">📤 Upload</button>
        </form>
        <div id="progress-container">
            <div id="progress-bar"></div>
        </div>
        <br>
        <a href="/gallery">📸 Xem thư viện</a>

        <script>
        const form = document.getElementById('uploadForm');
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const fileInput = form.querySelector('input[type=file]');
            if (!fileInput.files.length) return;

            const file = fileInput.files[0];
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            formData.append('file', file);

            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    progressContainer.style.display = 'block';
                    progressBar.style.width = percent + '%';
                }
            });

            xhr.onload = function() {
                if (xhr.status === 200) {
                    document.body.innerHTML = xhr.responseText;
                } else {
                    alert('❌ Upload thất bại');
                }
            };

            xhr.open('POST', '/', true);
            xhr.send(formData);
        });
        </script>
    </body>
    </html>
    ''')

# 🖼 Trang thư viện ảnh/video
@app.route('/gallery')
def gallery():
    try:
        results = Search()\
            .expression("resource_type:image OR resource_type:video")\
            .sort_by("created_at", "desc")\
            .max_results(50)\
            .execute()

        items = [r['secure_url'] for r in results['resources']]

        html = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>📸 Thư viện Cloudinary</title>
            <style>
                body { font-family: Arial; background: #f3f3f3; margin: 0; text-align: center; }
                h2 { background: #4CAF50; color: white; padding: 20px; margin: 0; }
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; padding: 20px; }
                .item { background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); padding: 10px; }
                img, video { width: 100%; border-radius: 10px; }
                a.btn { display: inline-block; margin: 15px auto; padding: 10px 20px; background: #4CAF50; color: white; border-radius: 8px; text-decoration: none; }
                a.btn:hover { background: #45a049; }
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
    app.run(debug=True)
