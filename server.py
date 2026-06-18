# -*- coding: utf-8 -*-
"""
server.py — okuma-yazma-asistani yerel sunucusu.
- Statik dosyalari ONBELLEKSIZ servis eder (degisiklikler aninda yansir).
- POST /log : Gemini'ye dusen (bankada olmayan) soru-cevaplari sorular.jsonl'a
  satir satir kaydeder (denetlenmek uzere).
Calistir:  python server.py     ->  http://127.0.0.1:8000/okuma-yazma-asistani.html
"""
import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = 8000
DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(DIR, "sorular.jsonl")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path in ("/", ""):
            self.path = "/okuma-yazma-asistani.html"
        return super().do_GET()

    def do_POST(self):
        if self.path != "/log":
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            obj = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            obj = {"raw": raw.decode("utf-8", "replace") if length else ""}
        obj["t"] = datetime.now().isoformat(timespec="seconds")
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *a):
        pass  # sessiz


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Sunucu calisiyor: http://127.0.0.1:{PORT}/okuma-yazma-asistani.html")
        print(f"Kayit dosyasi: {LOG_PATH}")
        httpd.serve_forever()
