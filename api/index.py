import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ---------------- CONFIG ----------------
DEVELOPER = "Creator Shyamchand & Ayan"
ORG = "CEO & Founder Of - Nexxon Hackers"
VERSION = "1.0.0"
IPIFY_URL = "https://api.ipify.org?format=json"

# ---------------- HTML TEMPLATE (Same Design as Provided) ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Own IP View API - Nexxon Hackers</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#3b82f6',secondary:'#1e40af'},borderRadius:{'button':'8px'}}}}</script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
</head>
<body class="bg-white min-h-screen">
<main class="pt-8 pb-8 px-4">
<header class="text-center py-8">
<h1 class="text-3xl font-bold text-gray-900 mb-2">Own IP View API</h1>
<p class="text-lg text-gray-600 mb-4">Fast & Reliable Public IP Detection Service</p>
<p class="text-sm text-gray-500 mb-6">Real-time IP Intelligence by Nexxon Hackers</p>
<div class="mb-6">
<img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc51?w=800&h=400&fit=crop" 
     alt="Network server" class="w-full h-48 object-cover object-center rounded-xl">
</div>
</header>

<section class="mb-8">
<div class="grid grid-cols-1 gap-4">
<div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
<div class="flex items-center">
<div class="w-12 h-12 flex items-center justify-center bg-blue-100 rounded-xl mr-4">
<i class="ri-shield-check-line text-blue-600 ri-xl"></i>
</div>
<div><h4 class="font-semibold text-gray-900">Secure Detection</h4><p class="text-sm text-gray-600">Encrypted IP Fetching</p></div>
</div>
</div>
<div class="bg-gradient-to-r from-purple-50 to-violet-50 rounded-xl p-6 border border-purple-100">
<div class="flex items-center">
<div class="w-12 h-12 flex items-center justify-center bg-purple-100 rounded-xl mr-4">
<i class="ri-pulse-line text-purple-600 ri-xl"></i>
</div>
<div><h4 class="font-semibold text-gray-900">High Performance</h4><p class="text-sm text-gray-600">Zero Latency Response</p></div>
</div>
</div>
</div>
</section>

<section class="mb-8">
<h2 class="text-xl font-bold text-gray-900 mb-6">API Endpoints</h2>
<div class="space-y-6">
<div class="bg-gray-50 rounded-xl p-6 border border-gray-200">
<div class="flex items-center justify-between mb-4">
<h3 class="font-semibold text-gray-900">View Your IP</h3>
<span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">GET</span>
</div>
<div class="bg-white rounded-lg p-4 border border-gray-200 mb-4">
<code class="text-sm text-gray-700">/view-ip</code>
</div>
<div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
<p class="text-sm font-medium text-blue-900 mb-2">📝 JSON Output Format:</p>
<pre class="text-xs text-blue-700">
{
  "api_info": { "developed_by": "...", "version": "1.0.0" },
  "ip": "8.8.8.8",
  "success": true,
  "timestamp": "..."
}
</pre>
</div>
</div>
</div>
</section>

<section class="mb-8">
<div class="bg-gradient-to-r from-primary to-secondary rounded-xl p-6 text-white text-center">
<h3 class="text-xl font-bold mb-2">Check Your IP Now</h3>
<p class="text-blue-100 text-sm mb-4">Click below to see your real-time public IP address</p>
<button id="tryApiBtn" class="bg-white text-primary px-6 py-3 rounded-button font-medium hover:bg-blue-50 transition">
Get My IP Address
</button>
</div>
</section>

<div class="text-center py-4 text-sm text-gray-500">
Developed by {{ dev }} | {{ org }}
</div>
</main>

<script>
document.getElementById('tryApiBtn').addEventListener('click', function() {
    fetch('/view-ip')
        .then(res => res.json())
        .then(data => {
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4';
            modal.innerHTML = `
                <div class="bg-white rounded-xl p-6 w-full max-w-md">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-gray-900">Your Live IP Address</h3>
                        <button onclick="this.parentElement.parentElement.parentElement.remove()">
                            <i class="ri-close-line text-gray-400 ri-lg"></i>
                        </button>
                    </div>
                    <div class="bg-gray-900 rounded-lg p-4 mb-4">
                        <pre class="text-xs text-green-400 overflow-x-auto">${JSON.stringify(data, null, 2)}</pre>
                    </div>
                    <p class="text-center text-xs text-gray-500">Nexxon Hackers Intelligence Service</p>
                </div>`;
            document.body.appendChild(modal);
        });
});
</script>
</body>
</html>
'''

# ---------------- FLASK ROUTES ----------------

@app.route('/')
def home():
    """ডিজাইনসহ ডকুমেন্টেশন পেজ"""
    return render_template_string(HTML_TEMPLATE, dev=DEVELOPER, org=ORG)

@app.route('/view-ip', methods=['GET'])
def get_own_ip():
    """ইউজারের আইপি ডাটা এন্ডপয়েন্ট"""
    try:
        # Ipify থেকে ডাটা নেয়া
        response = requests.get(IPIFY_URL, timeout=10)
        
        if response.status_code == 200:
            ip_data = response.json()
            detected_ip = ip_data.get('ip')
            
            # আপনার কাঙ্ক্ষিত JSON ফরম্যাট
            return jsonify({
                "api_info": {
                    "developed_by": DEVELOPER,
                    "organization": ORG,
                    "version": VERSION
                },
                "ip": detected_ip,
                "success": True,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        else:
            return jsonify({"success": False, "error": "External API connection failed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Vercel Handler
app_handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
