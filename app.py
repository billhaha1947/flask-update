from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary.utils
import os

app = Flask(__name__)

# --- Cấu hình Cloudinary (đặt key của bạn ở đây) ---
cloudinary.config(
    cloud_name="dma3eclgv",   # thay bằng của bạn
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
        return jsonify({'error': 'No file'}), 400
    try:
        res = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify({'url': res.get('secure_url'), 'public_id': res.get('public_id')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    try:
        # lấy images
        imgs = cloudinary.api.resources(type="upload", resource_type="image", max_results=100).get('resources', [])
        # lấy videos (resource_type video)
        vids = cloudinary.api.resources(type="upload", resource_type="video", max_results=100).get('resources', [])
        # lấy raw có thể chứa mp4/mov nếu người upload dùng resource_type=raw
        raws = cloudinary.api.resources(type="upload", resource_type="raw", max_results=100).get('resources', [])

        files = []

        # xử lý images
        for r in imgs:
            files.append({
                'type': 'image',
                'public_id': r.get('public_id'),
                'url': r.get('secure_url'),
                'format': r.get('format')
            })

        # xử lý videos (resource_type video) -> dùng secure_url nếu ok
        for r in vids:
            # đảm bảo có URL streamable (dùng cloudinary.utils để derive mp4 nếu cần)
            url = r.get('secure_url')
            # try derive mp4 URL (safer)
            try:
                derived = cloudinary.utils.cloudinary_url(r.get('public_id'), resource_type='video', format='mp4')[0]
                if derived:
                    url = derived
            except Exception:
                pass
            files.append({
                'type': 'video',
                'public_id': r.get('public_id'),
                'url': url,
                'format': r.get('format')
            })

        # xử lý raws: nếu format là mp4/mov/webm thì coi là video
        for r in raws:
            fmt = (r.get('format') or '').lower()
            if fmt in ['mp4', 'mov', 'webm', 'mkv']:
                # derive video url
                try:
                    url = cloudinary.utils.cloudinary_url(r.get('public_id'), resource_type='video', format='mp4')[0]
                except Exception:
                    url = r.get('secure_url') or r.get('url')
                files.append({
                    'type': 'video',
                    'public_id': r.get('public_id'),
                    'url': url,
                    'format': fmt
                })
            else:
                # nếu muốn hiển thị raw khác như pdf, you can skip or handle
                files.append({
                    'type': 'raw',
                    'public_id': r.get('public_id'),
                    'url': r.get('secure_url') or r.get('url'),
                    'format': fmt
                })

        # sắp xếp mới nhất trước
        files.sort(key=lambda x: x.get('public_id', ''), reverse=True)

        return render_template('gallery.html', files=files)
    except Exception as e:
        return f"<h3 style='color:red;'>Lỗi tải gallery: {e}</h3>"

@app.route('/delete/<public_id>', methods=['DELETE'])
def delete_file(public_id):
    password = request.args.get('password')
    # nếu bạn có ADMIN_PASSWORD cứng trong code, replace ở dưới
    ADMIN_PASSWORD = "xoa"
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Sai mật khẩu'}), 403
    try:
        # dùng resource_type='auto' để xóa cả image/video/raw
        result = cloudinary.uploader.destroy(public_id, resource_type='auto', invalidate=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
