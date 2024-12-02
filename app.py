#!/usr/bin/env python
# encoding: utf-8
import os
import signal
import json
from flask import Flask, request
#from ytmachine import LiveStreamPlayer
from players import MPVPlayer

app = Flask(__name__)
player = MPVPlayer()
player.main()

@app.route('/')
def index():
    return "<h1>Hello</h1><p>World!</p>"

@app.route('/play')
def play():
    player.play()
    return json.dumps({'state': 1})

@app.route('/pause')
def pause():
    player.pause()
    return json.dumps({'state': 2})

@app.route('/reload')
def reload():
    player.reload_video()
    return json.dumps({'state': 1, 'msg': "Video reloaded"})

@app.route('/purl')
def change_purl():
    npurl = request.args.get("permanent_url", False)
    if npurl:
        player.update_permanent_url(npurl)
    return json.dumps({'msg': "Permanent URL updated"})

@app.route('/shutdown')
def shutdown():
    print("Shutting down gracefully...")
    if player.state != 0:
        player.stop()
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)