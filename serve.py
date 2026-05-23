import os
os.chdir('/Users/alex/Desktop/website')

import json
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

DB = '/Users/alex/Desktop/website/florapark.db'

def init_db():
    c = sqlite3.connect(DB)
    c.execute('''CREATE TABLE IF NOT EXISTS submissions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, email TEXT, area TEXT,
        service TEXT, address TEXT, message TEXT,
        source TEXT, created_at TEXT)''')
    c.commit()
    c.close()

class H(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/submit':
            n = int(self.headers.get('Content-Length', 0))
            d = json.loads(self.rfile.read(n))
            c = sqlite3.connect(DB)
            c.execute(
                'INSERT INTO submissions(name,phone,email,area,service,address,message,source,created_at) VALUES(?,?,?,?,?,?,?,?,?)',
                (d.get('name',''), d.get('phone',''), d.get('email',''),
                 d.get('area',''), d.get('service',''), d.get('address',''),
                 d.get('message',''), d.get('source',''), datetime.now().isoformat()))
            c.commit()
            c.close()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

init_db()
HTTPServer(('', 8080), H).serve_forever()
