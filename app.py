#!/usr/bin/env python
# encoding: utf-8
import os
import signal
import json
from flask import Flask, request
import threading
from players import MPVPlayer

app = Flask(__name__)
player = MPVPlayer()
player.main()

white_noise_machine = None

def make_response(msg:str="OK", status:bool=True, extras={}):
    return {
        "msg": msg,
        "state": player.playing,
        "status": status,
        "wnm": True if white_noise_machine else False,
        "extras": extras
    }

def terminate_wnm():
    global white_noise_machine
    if white_noise_machine:
        white_noise_machine.stop()
        white_noise_machine = None

def start_timer(timer=7200.0):
    threading.Timer(timer, terminate_wnm).start()
    return True

@app.route('/')
def index():
    return "<h1>Hello</h1><p>World!</p>"

@app.route('/hello')
def hello():
    return json.dumps(make_response("Running"))

@app.route('/stats')
def stats():
    return json.dumps(make_response(extras={
        "playing": player.playing, 
        "muted": player.muted,
        "video": player.video,
        "mode": player.mode,
        "thread_health": player.is_alive(),
        "url": player.url}))

@app.route('/toggle')
def toggle():
    if white_noise_machine == None:
        player.toggle_play()
        return json.dumps(make_response("Success"))
    else:
        return json.dumps(make_response("WNM running", False))

@app.route('/mute')
def mute():
    player.toggle_mute()
    return json.dumps(make_response("Success"))

@app.route('/reload')
def reload():
    global player
    player.stop()
    player = MPVPlayer()
    player.main()
    return json.dumps(make_response("Video reloaded"))

@app.route('/change_mode')
def change_mode():
    if player.mode == 0:
        mode = 1
    else:
        mode = 0
    player.change_mode(mode)
    return json.dumps(make_response("Mode changed"))

@app.route('/change_video', methods=['POST'])
def change_video():
    data = request.get_json()
    print(data)
    video = data["video"]
    player.change_video(video)
    return json.dumps(make_response("Video changed"))

@app.route('/purl')
def change_purl():
    npurl = request.args.get("permanent_url", False)
    if npurl:
        player.update_permanent_url(npurl)
    return json.dumps(make_response("Permanent URL updated"))

@app.route('/shutdown')
def shutdown():
    print("Shutting down gracefully...")
    if player.state != 0:
        player.stop()
    os.kill(os.getpid(), signal.SIGINT)
    return json.dumps(make_response("Exited"))

@app.route('/noise_machine', methods=['POST'])
def noise_machine():
    global white_noise_machine
    if not player.playing and white_noise_machine == None:
        white_noise_machine = MPVPlayer(1)
        white_noise_machine.player._set_property("volume", 150)
        white_noise_machine.main()
        white_noise_machine.toggle_play()
        start_timer()
        return json.dumps(make_response("White noise machine started"))
    else:
        return json.dumps(make_response("White noise machine could not be started, pause player first", False))

@app.route('/stop_noise_machine', methods=['POST'])
def stop_noise_machine():
    print("Stopping")
    global white_noise_machine
    if white_noise_machine:
        white_noise_machine.stop()
        white_noise_machine = None
        return json.dumps(make_response("White noise machine stopped"))
    else:
        return json.dumps(make_response("Machine not running", False))

@app.route('/screenshot', methods=['POST'])
def screenshot():
    return json.dumps(make_response("White noise machine stopped"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)