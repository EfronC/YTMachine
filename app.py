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

@app.route('/hello')
def hello():
    return json.dumps({"status": True, "msg": "Running"})

@app.route('/play')
def play():
    player.play()
    return json.dumps({'state': 1})

@app.route('/pause')
def pause():
    player.pause()
    return json.dumps({'state': 2})

@app.route('/toggle')
def toggle():
    player.toggle_play()
    return json.dumps({'state': 2, "msg": "Ok"})

@app.route('/reload')
def reload():
    player.reload_video()
    return json.dumps({'state': 1, 'msg': "Video reloaded"})

@app.route('/change_mode')
def change_mode():
    if player.mode == 0:
        mode = 1
    else:
        mode = 0
    player.change_mode(mode)
    return json.dumps({'state': 1, 'msg': "Mode changed"})

@app.route('/change_video', methods=['POST'])
def change_video():
    data = request.get_json()
    video = data["video"]
    player.change_video(video)
    return json.dumps({'state': 1, 'msg': "Video changed"})

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
    return json.dumps({'msg': "Exited"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)