from flask import Flask, render_template
import cloudinary
import os

app = Flask(__name__)

# ⚙️ Cấu hình Cloudinary từ biến môi trường Render
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    # Lấy ảnh từ Cloudinary (lấy 50 ảnh gần nhất)
    from cloudinary.api import resources
    result = resources(max_results=50)
    return render_template('gallery.html', resources=result['resources'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
