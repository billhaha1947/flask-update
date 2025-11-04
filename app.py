from cloudinary import Search

@app.route('/gallery')
def gallery():
    try:
        # Tìm tất cả file upload gần nhất
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
