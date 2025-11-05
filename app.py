# app.py
from flask import Flask, render_template_string
import cloudinary
import cloudinary.api
import os
import traceback

app = Flask(__name__)

# ---------- CẤU HÌNH CLOUDINARY -----------
# Option A: hardcode (thay bằng thông tin của bạn)
cloudinary.config(
    cloud_name="dma3eclgv",
    api_key="118974677734641",
    api_secret="8Dhe37EYtXQVaaPpCsDIRRZSrE4"
)

# Option B (thay thế): nếu bạn muốn dùng ENV vars thay hardcode,
# uncomment đoạn bên dưới và comment đoạn hardcode ở trên.
# cloudinary.config(
#     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.getenv("CLOUDINARY_API_KEY"),
#     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# )

print("DEBUG: Cloudinary cloud_name:", cloudinary.config().cloud_name)
print("DEBUG: Cloudinary api_key set?:", bool(cloudinary.config().api_key))
# Không print api_secret lên log (bảo mật)

# ---------- ROUTES ----------
INDEX_HTML = """
<!doctype html>
<title>Index</title>
<h2>Trang chính</h2>
<p><a href="/gallery">Xem gallery</a></p>
"""

ERROR_HTML = """
<!doctype html>
<title>Lỗi</title>
<h2>Lỗi khi tải gallery</h2>
<p style="color:crimson">Có lỗi xảy ra ở server. Mở logs để xem chi tiết.</p>
<p><a href="/">Về trang chính</a></p>
"""

GALLERY_HTML_START = """
<!doctype html>
<title>Gallery</title>
<h1>📸 Thư viện ảnh</h1>
<p><a href="/">⬅ Quay lại</a></p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;">
"""

GALLERY_HTML_END = "</div>"

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/gallery")
def gallery():
    try:
        # Lấy resources (upload type). Nếu muốn lấy cả image+video dùng type='upload'
        # tăng max_results nếu cần
        resp = cloudinary.api.resources(type="upload", max_results=100)
        resources = resp.get("resources", [])
        print(f"DEBUG: fetched {len(resources)} resources")
        html = GALLERY_HTML_START
        for r in resources:
            r_type = r.get("resource_type", "")
            url = r.get("secure_url") or r.get("url")
            if not url:
                continue
            if r_type == "video":
                html += f'<video controls style="width:100%;height:200px;object-fit:cover;border-radius:8px;"><source src="{url}"></video>'
            else:
                html += f'<img src="{url}" style="width:100%;height:200px;object-fit:cover;border-radius:8px;">'
        html += GALLERY_HTML_END
        return render_template_string(html)
    except Exception as e:
        # In traceback đầy đủ ra logs (Render sẽ hiển thị)
        tb = traceback.format_exc()
        print("ERROR in /gallery:", str(e))
        print(tb)
        # Phân biệt lỗi 401 Authorization
        msg = str(e)
        if "AuthorizationRequired" in msg or "api_secret" in msg or "401" in msg or "api_key" in msg:
            # Gợi ý cụ thể cho user
            print("DEBUG: Có khả năng API key / API secret không chính xác. Kiểm tra Environment Variables hoặc giá trị hardcoded.")
        return render_template_string(ERROR_HTML), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
