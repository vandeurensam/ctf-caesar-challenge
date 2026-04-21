#!/usr/bin/env python3
"""
HTTP Headers & Cookies CTF Challenge
Find the flag hidden in HTTP response headers or cookies
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# The flag hidden in headers
FLAG = "CTF{http_h34d3r_s3cr3t}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HTTP Headers Challenge</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            text-align: center;
        }
        .hint {
            background: #f0f0f0;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        .info-box {
            background: #e8f4f8;
            border: 1px solid #b0d4e0;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px 10px 0;
        }
        button:hover {
            background: #764ba2;
        }
        .response {
            background: #f9f9f9;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            display: none;
        }
        .response.show {
            display: block;
        }
        #result {
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background: #d4edda;
            color: #155724;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 HTTP Headers & Cookies Challenge</h1>
        
        <div class="hint">
            <strong>Challenge:</strong> A flag is hidden somewhere in the HTTP response. 
            It could be in headers, cookies, or even the response body. Find it!
        </div>
        
        <div class="info-box">
            <strong>What you need to know:</strong>
            <ul>
                <li>HTTP Headers are metadata sent with responses</li>
                <li>Cookies are stored in headers and browsers</li>
                <li>Some information might not be visible in the browser</li>
                <li>Use browser developer tools (F12) to inspect</li>
            </ul>
        </div>
        
        <h2>Investigation Tools</h2>
        
        <button onclick="fetchHeaders()">Fetch Response Headers</button>
        <button onclick="checkCookies()">Check Cookies</button>
        <button onclick="inspectResponse()">Inspect Full Response</button>
        
        <div id="response" class="response">
            <h3>Response Data:</h3>
            <div class="code-block" id="responseData"></div>
            <div id="result"></div>
        </div>
        
        <div class="hint" style="margin-top: 30px;">
            <strong>Browser Dev Tools Tips:</strong>
            <ol>
                <li>Press F12 or right-click → Inspect</li>
                <li>Go to Network tab</li>
                <li>Refresh the page</li>
                <li>Click on the request and check Response Headers</li>
                <li>Look for suspicious headers!</li>
            </ol>
        </div>
    </div>
    
    <script>
        function fetchHeaders() {
            fetch('/api/headers')
                .then(response => {
                    let headerText = 'Response Headers:\\n' + '-'.repeat(50) + '\\n';
                    for (let [key, value] of response.headers) {
                        headerText += `${key}: ${value}\\n`;
                    }
                    document.getElementById('responseData').textContent = headerText;
                    document.getElementById('response').classList.add('show');
                    checkForFlag(headerText);
                })
                .catch(err => {
                    document.getElementById('responseData').textContent = 'Error: ' + err;
                    document.getElementById('response').classList.add('show');
                });
        }
        
        function checkCookies() {
            fetch('/api/cookies')
                .then(r => r.json())
                .then(data => {
                    let cookieText = 'Cookies:\\n' + '-'.repeat(50) + '\\n';
                    for (let key in data.cookies) {
                        cookieText += `${key}: ${data.cookies[key]}\\n`;
                    }
                    document.getElementById('responseData').textContent = cookieText;
                    document.getElementById('response').classList.add('show');
                    checkForFlag(cookieText);
                });
        }
        
        function inspectResponse() {
            fetch('/api/inspect')
                .then(r => r.json())
                .then(data => {
                    let inspectText = 'Full Response Inspection:\\n' + '-'.repeat(50) + '\\n';
                    inspectText += JSON.stringify(data, null, 2);
                    document.getElementById('responseData').textContent = inspectText;
                    document.getElementById('response').classList.add('show');
                    checkForFlag(inspectText);
                });
        }
        
        function checkForFlag(text) {
            if (text.includes('CTF{')) {
                const match = text.match(/CTF{[^}]+}/);
                if (match) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.className = 'success';
                    resultDiv.textContent = '✓ FLAG FOUND: ' + match[0];
                }
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main challenge page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/headers')
def api_headers():
    """Return headers with flag hidden"""
    response = jsonify({"message": "Check the headers!"})
    response.headers['X-Flag-Part-1'] = 'CTF{'
    response.headers['X-Flag-Part-2'] = 'http_'
    response.headers['X-Flag-Part-3'] = 'h34d3r_'
    response.headers['X-Secret'] = 's3cr3t}'
    response.headers['X-Challenge'] = 'Combine the X-Flag-* headers with X-Secret'
    return response

@app.route('/api/cookies')
def api_cookies():
    """Return cookies with flag hidden"""
    response = jsonify({
        "cookies": {
            "session_id": "abc123xyz",
            "user": "player",
            "flag_part": "CTF{http_h34d3r_s3cr3t}"
        }
    })
    response.set_cookie('flag_hint', 'check_headers', max_age=3600)
    response.set_cookie('X-Flag', FLAG, max_age=3600)
    return response

@app.route('/api/inspect')
def api_inspect():
    """Return inspection data with flag"""
    return jsonify({
        "challenge": "HTTP Headers & Cookies",
        "difficulty": "Easy",
        "hint": "Look at response headers and cookies",
        "flag": FLAG,
        "message": "The flag is hidden in plain sight across multiple response headers and cookies"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("=" * 60)
    print("HTTP HEADERS & COOKIES CHALLENGE")
    print("=" * 60)
    print()
    print("Server starting on http://localhost:5000")
    print()
    print("Challenge: Find the flag hidden in HTTP headers/cookies")
    print()
    print("Open http://localhost:5000 in your browser")
    print("Use browser DevTools (F12) or the provided tools")
    print()
    app.run(host='0.0.0.0', port=5000, debug=False)
