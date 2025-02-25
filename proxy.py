from flask import Flask, request, Response, render_template_string
import requests
from urllib.parse import urljoin

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Proxy</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; font-family: Arial, sans-serif; }
        input { width: 300px; padding: 10px; }
        button { padding: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Enter a URL</h1>
    <form method="GET" action="/proxy">
        <input type="text" name="url" placeholder="Enter full URL" required>
        <button type="submit">Go</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "No URL provided", 400
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    try:
        response = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for name, value in response.headers.items() if name.lower() not in excluded_headers]
        return Response(response.content, response.status_code, headers)
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
