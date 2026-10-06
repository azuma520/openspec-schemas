"""Minimal OTLP http/json receiver: appends each POST body (with path and receive time) to a JSONL file.

Usage: python collector.py <port> <out.jsonl>
Accepts /v1/logs, /v1/metrics, /v1/traces; always answers 200 {}.
"""
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
OUT = sys.argv[2]


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            body = {"_unparsed": raw[:2000].decode("utf-8", "replace"),
                    "_content_type": self.headers.get("Content-Type")}
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps({"path": self.path, "received": time.time(), "body": body},
                               ensure_ascii=False) + "\n")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", PORT), H).serve_forever()
