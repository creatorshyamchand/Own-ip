import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# ---------------- CONFIG ----------------
IPIFY_URL = "https://api.ipify.org?format=json"

# ---------------- HELPER FUNCTIONS ----------------
def get_client_ip():
    """Get real client IP from various sources"""
    try:
        # Try multiple sources for accuracy
        sources = []
        
        # Source 1: Request headers
        if request.headers.get('X-Forwarded-For'):
            ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
            if ip and ip != '127.0.0.1' and ip != '::1':
                sources.append({'source': 'X-Forwarded-For', 'ip': ip})
        
        if request.headers.get('X-Real-IP'):
            ip = request.headers.get('X-Real-IP').strip()
            if ip and ip != '127.0.0.1' and ip != '::1':
                sources.append({'source': 'X-Real-IP', 'ip': ip})
        
        # Source 2: Remote address
        remote_ip = request.remote_addr
        if remote_ip and remote_ip != '127.0.0.1' and remote_ip != '::1':
            sources.append({'source': 'Remote Address', 'ip': remote_ip})
        
        # Source 3: ipify.org (external service)
        try:
            response = requests.get(IPIFY_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                ipify_ip = data.get('ip')
                if ipify_ip:
                    sources.append({'source': 'ipify.org', 'ip': ipify_ip})
        except:
            pass
        
        # Determine the most reliable IP
        primary_ip = None
        if sources:
            # Prefer ipify.org as it sees the actual public IP
            for s in sources:
                if s['source'] == 'ipify.org':
                    primary_ip = s['ip']
                    break
            if not primary_ip:
                primary_ip = sources[0]['ip']
        
        return {
            'success': True,
            'ip': primary_ip or 'Unable to detect',
            'detected_from': [s['source'] for s in sources],
            'all_sources': sources,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'api_info': {
                'developed_by': 'Creator Shyamchand & Ayan',
                'organization': 'CEO & Founder Of - Nexxon Hackers',
                'version': '1.0.0'
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'api_info': {
                'developed_by': 'Creator Shyamchand & Ayan',
                'organization': 'CEO & Founder Of - Nexxon Hackers'
            }
        }

# ---------------- HTML TEMPLATE ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My IP API - Nexxon Hackers</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#8b5cf6',secondary:'#6d28d9'},borderRadius:{'none':'0px','sm':'4px',DEFAULT:'8px','md':'12px','lg':'16px','xl':'20px','2xl':'24px','3xl':'32px','full':'9999px','button':'8px'}}}}</script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
<style>
.loading-spinner {
    border: 2px solid #f3f3f3;
    border-top: 2px solid #8b5cf6;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
    display: inline-block;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.json-viewer {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 13px;
    line-height: 1.5;
}
.json-key { color: #9cdcfe; }
.json-string { color: #ce9178; }
.json-number { color: #b5cea8; }
.json-boolean { color: #569cd6; }
.json-null { color: #569cd6; }
.glow-text {
    text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
}
</style>
</head>
<body class="bg-gradient-to-br from-purple-50 via-white to-indigo-50 min-h-screen">
<main class="pt-8 pb-12 px-4 max-w-4xl mx-auto">
    
    <!-- Header -->
    <header class="text-center py-8">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary to-secondary rounded-3xl mb-6 shadow-lg">
            <i class="ri-user-location-line text-white ri-3x"></i>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2 glow-text">My IP API</h1>
        <p class="text-lg text-gray-600 mb-4">Instantly Get Your Public IP Address</p>
        <p class="text-sm text-gray-500">Simple • Fast • Reliable</p>
    </header>

    <!-- Live Test Section -->
    <section class="mb-8 bg-white rounded-3xl p-8 shadow-xl border border-purple-100">
        <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <i class="ri-radar-line text-primary mr-2"></i>
            Your Current IP Address
        </h2>
        
        <div class="text-center mb-6">
            <button id="getIpBtn" class="bg-gradient-to-r from-primary to-secondary text-white px-8 py-4 rounded-xl font-medium hover:shadow-lg transition-all transform hover:scale-105 flex items-center justify-center gap-3 mx-auto">
                <i class="ri-refresh-line"></i>
                <span>Detect My IP</span>
            </button>
        </div>
        
        <div id="loadingIndicator" class="hidden text-center py-8">
            <div class="loading-spinner w-8 h-8"></div>
            <span class="ml-3 text-gray-500">Detecting your IP address...</span>
        </div>
        
        <div id="ipDisplay" class="hidden">
            <div class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl p-6 border border-purple-200 mb-4">
                <p class="text-sm text-gray-600 mb-2">Your Public IP Address:</p>
                <div class="flex items-center justify-center gap-4">
                    <code id="ipAddress" class="text-4xl font-mono font-bold text-primary"></code>
                    <button id="copyIpBtn" class="bg-white p-2 rounded-lg shadow-sm hover:shadow transition" title="Copy IP">
                        <i class="ri-file-copy-line text-gray-600"></i>
                    </button>
                </div>
            </div>
            
            <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">Full Response:</span>
                <button id="copyJsonBtn" class="text-xs text-primary hover:text-secondary flex items-center gap-1">
                    <i class="ri-file-copy-line"></i> Copy JSON
                </button>
            </div>
            <pre id="jsonDisplay" class="json-viewer"></pre>
        </div>
        
        <div id="errorDisplay" class="hidden bg-red-50 border border-red-200 rounded-xl p-4 text-red-700"></div>
    </section>

    <!-- Features Grid -->
    <section class="mb-8">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-white rounded-xl p-5 border border-purple-100 shadow-sm">
                <div class="flex items-center">
                    <div class="w-10 h-10 flex items-center justify-center bg-purple-100 rounded-xl mr-3">
                        <i class="ri-flashlight-line text-purple-600 ri-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-semibold text-gray-900">Instant Detection</h4>
                        <p class="text-xs text-gray-600">Real-time IP lookup</p>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-xl p-5 border border-indigo-100 shadow-sm">
                <div class="flex items-center">
                    <div class="w-10 h-10 flex items-center justify-center bg-indigo-100 rounded-xl mr-3">
                        <i class="ri-shield-check-line text-indigo-600 ri-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-semibold text-gray-900">Multiple Sources</h4>
                        <p class="text-xs text-gray-600">Cross-verified accuracy</p>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-xl p-5 border border-pink-100 shadow-sm">
                <div class="flex items-center">
                    <div class="w-10 h-10 flex items-center justify-center bg-pink-100 rounded-xl mr-3">
                        <i class="ri-code-line text-pink-600 ri-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-semibold text-gray-900">JSON Response</h4>
                        <p class="text-xs text-gray-600">Easy API integration</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- API Endpoint -->
    <section class="mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4">API Endpoint</h2>
        <div class="bg-white rounded-2xl p-6 border border-purple-100 shadow-sm">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900">Get Your IP Address</h3>
                <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">GET</span>
            </div>
            <div class="bg-gray-900 rounded-lg p-4 mb-4">
                <code class="text-green-400 text-sm">/api/myip</code>
            </div>
            <div class="bg-purple-50 rounded-lg p-4 border border-purple-200">
                <p class="text-xs font-medium text-purple-900 mb-2">Example Request:</p>
                <code class="text-xs text-purple-700">curl "https://api.example.com/api/myip"</code>
            </div>
        </div>
    </section>

    <!-- Sample Response -->
    <section class="mb-8 bg-white rounded-2xl p-6 shadow-sm border border-purple-100">
        <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <i class="ri-braces-line text-primary mr-2"></i>
            Sample Response
        </h2>
        <pre class="json-viewer text-xs">{
  "success": true,
  "ip": "157.34.202.198",
  "detected_from": ["ipify.org", "X-Forwarded-For"],
  "all_sources": [
    {"source": "X-Forwarded-For", "ip": "157.34.202.198"},
    {"source": "ipify.org", "ip": "157.34.202.198"}
  ],
  "timestamp": "2024-01-15T10:30:45.123Z",
  "api_info": {
    "developed_by": "Creator Shyamchand & Ayan",
    "organization": "CEO & Founder Of - Nexxon Hackers",
    "version": "1.0.0"
  }
}</pre>
    </section>

    <!-- Developer Team Image -->
    <section class="mb-8">
        <div class="bg-gradient-to-br from-purple-100 to-indigo-100 rounded-3xl p-6 border border-purple-200">
            <h3 class="text-lg font-bold text-gray-900 mb-4 text-center">Powered By Nexxon Hackers Team</h3>
            <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=400&fit=crop" 
                 alt="Nexxon Hackers Development Team" 
                 class="w-full h-48 object-cover object-top rounded-xl shadow-md">
            <p class="text-center text-sm text-gray-600 mt-4">Our expert team building innovative solutions</p>
        </div>
    </section>

    <!-- Developer Credit -->
    <div class="text-center py-6">
        <div class="inline-block bg-gradient-to-r from-primary to-secondary text-white px-8 py-4 rounded-2xl shadow-lg">
            <p class="font-bold text-lg">Developed by Creator Shyamchand & Ayan</p>
            <p class="text-sm opacity-95">CEO & Founder Of - Nexxon Hackers</p>
        </div>
    </div>

</main>

<script>
function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, function (match) {
        var cls = 'json-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'json-key';
                match = match.slice(0, -1) + '</span>:';
                return '<span class="' + cls + '">' + match;
            } else {
                cls = 'json-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'json-boolean';
        } else if (/null/.test(match)) {
            cls = 'json-null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

async function fetchMyIp() {
    const ipDisplay = document.getElementById('ipDisplay');
    const ipAddress = document.getElementById('ipAddress');
    const jsonDisplay = document.getElementById('jsonDisplay');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorDisplay = document.getElementById('errorDisplay');
    const getIpBtn = document.getElementById('getIpBtn');
    
    ipDisplay.classList.add('hidden');
    errorDisplay.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    getIpBtn.disabled = true;
    
    try {
        const response = await fetch('/api/myip');
        const data = await response.json();
        
        loadingIndicator.classList.add('hidden');
        getIpBtn.disabled = false;
        
        if (data.success) {
            ipAddress.textContent = data.ip;
            
            const jsonStr = JSON.stringify(data, null, 2);
            jsonDisplay.innerHTML = syntaxHighlight(jsonStr);
            ipDisplay.classList.remove('hidden');
        } else {
            errorDisplay.textContent = 'Error: ' + (data.error || 'Failed to detect IP');
            errorDisplay.classList.remove('hidden');
        }
        
    } catch (error) {
        loadingIndicator.classList.add('hidden');
        getIpBtn.disabled = false;
        errorDisplay.textContent = 'Network Error: ' + error.message;
        errorDisplay.classList.remove('hidden');
    }
}

document.getElementById('getIpBtn').addEventListener('click', fetchMyIp);

document.getElementById('copyIpBtn').addEventListener('click', function() {
    const ipText = document.getElementById('ipAddress').textContent;
    navigator.clipboard.writeText(ipText).then(() => {
        const btn = document.getElementById('copyIpBtn');
        btn.innerHTML = '<i class="ri-check-line text-green-600"></i>';
        setTimeout(() => {
            btn.innerHTML = '<i class="ri-file-copy-line text-gray-600"></i>';
        }, 2000);
    });
});

document.getElementById('copyJsonBtn').addEventListener('click', function() {
    const jsonText = document.getElementById('jsonDisplay').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        const btn = document.getElementById('copyJsonBtn');
        btn.innerHTML = '<i class="ri-check-line"></i> Copied!';
        setTimeout(() => {
            btn.innerHTML = '<i class="ri-file-copy-line"></i> Copy JSON';
        }, 2000);
    });
});

// Auto-fetch on page load
window.addEventListener('load', function() {
    setTimeout(fetchMyIp, 500);
});
</script>
</body>
</html>
'''

# ---------------- FLASK ROUTES ----------------
@app.route('/')
def home():
    """Home page with API documentation"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/myip', methods=['GET'])
def get_my_ip():
    """Get client's public IP address"""
    result = get_client_ip()
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "My IP API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": {
            "home": "/",
            "my_ip": "/api/myip",
            "health": "/api/health"
        },
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
