import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# ---------------- CONFIG ----------------
DEVELOPER = "Creator Shyamchand & Ayan"
ORG = "CEO & Founder Of - Nexxon Hackers"
VERSION = "1.0.0"

# ---------------- HTML TEMPLATE (Hoboho Same to your Design) ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IP Information API - Advanced Geolocation Service</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#3b82f6',secondary:'#1e40af'},borderRadius:{'none':'0px','sm':'4px',DEFAULT:'8px','md':'12px','lg':'16px','xl':'20px','2xl':'24px','3xl':'32px','full':'9999px','button':'8px'}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
<style>
:where([class^="ri-"])::before {
content: "\f3c2";
}
</style>
</head>
<body class="bg-white min-h-screen">
<main class="pt-8 pb-8 px-4">
<header class="text-center py-8">
<h1 class="text-3xl font-bold text-gray-900 mb-2">Own IP View API</h1>
<p class="text-lg text-gray-600 mb-4">Advanced IP Geolocation & Intelligence Service</p>
<p class="text-sm text-gray-500 mb-6">Precise Location Data & Real-time Intelligence</p>
<div class="mb-6">
<img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=400&fit=crop" 
     alt="Developers collaborating" 
     class="w-full h-48 object-cover object-top rounded-xl">
</div>
</header>
<section class="mb-8">
<div class="grid grid-cols-1 gap-4">
<div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
<div class="flex items-center mb-3">
<div class="w-12 h-12 flex items-center justify-center bg-blue-100 rounded-xl mr-4">
<i class="ri-map-pin-line text-blue-600 ri-xl"></i>
</div>
<div>
<h4 class="font-semibold text-gray-900">Precise Location</h4>
<p class="text-sm text-gray-600">City, Region & Coordinates</p>
</div>
</div>
</div>
<div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
<div class="flex items-center mb-3">
<div class="w-12 h-12 flex items-center justify-center bg-green-100 rounded-xl mr-4">
<i class="ri-map-2-line text-green-600 ri-xl"></i>
</div>
<div>
<h4 class="font-semibold text-gray-900">Google Maps</h4>
<p class="text-sm text-gray-600">Direct Map Integration</p>
</div>
</div>
</div>
<div class="bg-gradient-to-r from-purple-50 to-violet-50 rounded-xl p-6 border border-purple-100">
<div class="flex items-center mb-3">
<div class="w-12 h-12 flex items-center justify-center bg-purple-100 rounded-xl mr-4">
<i class="ri-flashlight-line text-purple-600 ri-xl"></i>
</div>
<div>
<h4 class="font-semibold text-gray-900">Batch Support</h4>
<p class="text-sm text-gray-600">Multiple IPs at Once</p>
</div>
</div>
</div>
</div>
</section>
<section class="mb-8">
<h2 class="text-xl font-bold text-gray-900 mb-6">API Endpoints</h2>
<div class="space-y-6">
<div class="bg-gray-50 rounded-xl p-6 border border-gray-200">
<div class="flex items-center justify-between mb-4">
<h3 class="font-semibold text-gray-900">Get Your Own IP</h3>
<span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">GET</span>
</div>
<div class="bg-white rounded-lg p-4 border border-gray-200 mb-4">
<code class="text-sm text-gray-700">/view-ip</code>
</div>
<div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
<p class="text-sm font-medium text-blue-900 mb-2">📝 Example Response:</p>
<pre class="text-xs text-blue-700 overflow-x-auto">
{
  "api_info": { "developed_by": "Creator Shyamchand & Ayan", ... },
  "ip": "YOUR_IP_ADDRESS",
  "success": true,
  "timestamp": "2026-04-17..."
}
</pre>
</div>
</div>
</div>
</section>
<section class="mb-8">
<div class="bg-gradient-to-r from-primary to-secondary rounded-xl p-6 text-white text-center">
<div class="mb-4">
<div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
<i class="ri-code-s-slash-line text-white ri-2x"></i>
</div>
<h3 class="text-xl font-bold mb-2">Try Our API</h3>
<p class="text-blue-100 text-sm mb-4">Test the endpoints with your own IP address</p>
</div>
<button id="tryApiBtn" class="bg-white text-primary px-6 py-3 rounded-button font-medium cursor-pointer !rounded-button hover:bg-blue-50 transition">
Get Started Now
</button>
</div>
</section>
<div class="text-center py-4">
<p class="text-sm text-gray-500">Developed by Creator Shyamchand & Ayan | CEO & Founder Of - Nexxon Hackers</p>
</div>
</main>
<script>
document.getElementById('tryApiBtn').addEventListener('click', function() {
    fetch('/view-ip')
        .then(res => res.json())
        .then(data => {
            const demoModal = document.createElement('div');
            demoModal.className = 'fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4';
            demoModal.innerHTML = `
                <div class="bg-white rounded-xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-bold text-gray-900">API Demo - Your IP</h3>
                        <button onclick="this.parentElement.parentElement.parentElement.remove()" class="w-8 h-8 flex items-center justify-center cursor-pointer">
                            <i class="ri-close-line text-gray-400 ri-lg"></i>
                        </button>
                    </div>
                    <div class="bg-gray-900 rounded-lg p-4 mb-4">
                        <pre class="text-xs text-green-400 overflow-x-auto">${JSON.stringify(data, null, 2)}</pre>
                    </div>
                    <button onclick="navigator.clipboard.writeText('${data.ip}'); alert('IP Copied!')" class="w-full bg-primary text-white py-3 rounded-button font-medium">
                        Copy IP Address
                    </button>
                </div>
            `;
            document.body.appendChild(demoModal);
        });
});
</script>
</body>
</html>
'''

# ---------------- FLASK ROUTES ----------------

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/view-ip', methods=['GET'])
def get_my_ip():
    """Vercel Proxy bypass করে আসল ইউজার আইপি ডিটেক্ট করবে"""
    try:
        # Vercel বা অন্য প্রক্সির মাধ্যমে আসল আইপি বের করা
        if request.headers.get('X-Forwarded-For'):
            client_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            client_ip = request.remote_addr
            
        return jsonify({
            "api_info": {
                "developed_by": DEVELOPER,
                "organization": ORG,
                "version": VERSION
            },
            "ip": client_ip,
            "success": True,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Vercel handler
app_handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
