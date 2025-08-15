#!/usr/bin/env python
# encoding: utf-8
import os
import signal
import json
from flask import Flask, request, jsonify
import threading
from players import MPVPlayer, WNMPlayer
from screenshot import get_screenshot

app = Flask(__name__)
player = MPVPlayer()
player.main()

SONGS = {}
CURRENT_SONG = "./songs/Minecraft_Sweden.mp3"

white_noise_machine = None

def make_response(msg:str="OK", status:bool=True, extras={}):
    return {
        "msg": msg,
        "state": player.playing,
        "status": status,
        "wnm": True if white_noise_machine else False,
        "data": extras
    }

def terminate_wnm():
    global white_noise_machine
    if white_noise_machine:
        white_noise_machine.stop()
        white_noise_machine = None

def start_timer(timer=7200.0):
    threading.Timer(timer, terminate_wnm).start()
    return True

def update_video_list() -> bool:
    try:
        global SONGS
        SONGS = {}
        for i in os.listdir("./songs"):
            key = i.split(".")[0]
            SONGS[key] = i
        return True
    except Exception as e:
        print(e)
        return False

def reload_player(mode: int, video: str = "./songs/Minecraft_Sweden.mp3") -> bool:
    try:
        global player

        player.stop()
        player = MPVPlayer(mode, video)
        player.main()
        player.toggle_play()
    except Exception as e:
        raise e

@app.route('/')
def index():
    return "<h1>Hello</h1><p>World!</p>"

@app.route('/hello')
def hello():
    return jsonify(make_response("Running"))

@app.route('/stats')
def stats():
    update_video_list()
    return jsonify(make_response(extras={
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
        return jsonify(make_response("Success"))
    else:
        return jsonify(make_response("WNM running", False))

@app.route('/mute')
def mute():
    player.toggle_mute()
    return jsonify(make_response("Success"))

@app.route('/reload')
def reload():
    global player
    player.stop()
    player = MPVPlayer()
    player.main()
    return jsonify(make_response("Video reloaded"))

@app.route('/change_mode')
def change_mode():
    if player.mode == 0:
        reload_player(1)
    else:
        reload_player(0)
    return jsonify(make_response("Mode changed"))

@app.route('/change_video', methods=['POST'])
def change_video():
    try:
        data = request.get_json()
        if data["mode"] == 1:
            global CURRENT_SONG
            global white_noise_machine
            video = data["video"]
            CURRENT_SONG = "./songs/"+SONGS[video]
        else:
            video = data["video"]
            player.update_permanent_url(video)
            reload_player(0)
    except Exception as e:
        print(e)
    return jsonify(make_response("Video changed"))

@app.route('/list_videos', methods=['GET'])
def list_videos():
    return jsonify(make_response("Videos", True, SONGS))

@app.route('/shutdown')
def shutdown():
    print("Shutting down gracefully...")
    player.stop()
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify(make_response("Exited"))

@app.route('/noise_machine', methods=['POST'])
def noise_machine():
    global white_noise_machine
    if not player.playing and white_noise_machine == None:
        white_noise_machine = WNMPlayer(video=CURRENT_SONG)
        white_noise_machine.player._set_property("volume", 150)
        white_noise_machine.main()
        white_noise_machine.toggle_play()
        start_timer()
        return jsonify(make_response("White noise machine started"))
    else:
        return jsonify(make_response("White noise machine could not be started, pause player first", False))

@app.route('/stop_noise_machine', methods=['POST'])
def stop_noise_machine():
    print("Stopping")
    global white_noise_machine
    if white_noise_machine:
        white_noise_machine.stop()
        white_noise_machine = None
        return jsonify(make_response("White noise machine stopped"))
    else:
        return jsonify(make_response("Machine not running", False))

@app.route('/current_nm_song')
def current_nm_song():
    global white_noise_machine
    if white_noise_machine:
        return jsonify(make_response(white_noise_machine.video.split("/")[-1]))
    else:
        return jsonify(make_response("Machine not running", False))

@app.route('/video_id', methods=['GET'])
def video_id():
    url = player.get_video_id(player.url)
    video_id = url.split("?")[1].split("=")[1]
    return jsonify(make_response("Success", True, {
        "video_id": video_id
        }))

if __name__ == '__main__':
    update_video_list()
    app.run(host='0.0.0.0', port=5000, threaded=True)