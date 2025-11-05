from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return redirect(url_for('gallery'))
    return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    # Lấy danh sách ảnh/video từ Cloudinary
    resources = cloudinary.api.resources(type="upload", max_results=100)
    media = resources.get('resources', [])
    return render_template('gallery.html', media=media)

if __name__ == '__main__':
    app.run(debug=True)
