#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask
from ytmachine import LiveStreamPlayer

app = Flask(__name__)
lsp = LiveStreamPlayer()
lsp.main()

@app.route('/')
def index():
    return "<h1>Hello</h1><p>World!</p>"

@app.route('/play')
def play():
    lsp.play()
    return json.dumps({'state': 1})

@app.route('/pause')
def pause():
    lsp.pause()
    return json.dumps({'state': 2})

@app.route('/stop')
def stop():
    lsp.stop()
    return json.dumps({'state': 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)