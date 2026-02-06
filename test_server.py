#!/usr/bin/env python3
"""
Simple HTTP server to test the GitHub Pages deployment locally
Run: python test_server.py
Then visit: http://localhost:8000
"""

import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "docs"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Finlytics Test Server Running!")
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"📁 Serving: {DIRECTORY}/")
        print(f"⏹️  Press Ctrl+C to stop")
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped")
