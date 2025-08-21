import threading
import json
import requests
from bs4 import BeautifulSoup
import mpv
import time
from datetime import datetime
import os
from logger import logger

LOG_FILE = "player_errors.log"

def log_error(message: str):
    """Append error message to log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)  # Still print to console

def log_MPV_message(level: str, prefix: str, text: str):
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # with open(LOG_FILE, "a", encoding="utf-8") as f:
    #     f.write(f"[{timestamp}]({level}) {prefix}: {text[:-1]}\n")
    msg = f"({level}) {prefix}: {text.rstrip()}"
    logger.error(msg)

class Player:
    def __init__(self):
        self.state = 0
        self.player = None
        self.url = None

    def update_permanent_url(self, url: str):
        try:
            data = self.read_json("data.json")
            data["permanent_url"] = url
            self.write_json(data, "data.json")
            return True
        except Exception as e:
            log_error(str(e))
            return False

    def get_video_stream(self):
        try:
            data = self.read_json("data.json")
            url = self.get_video_id(data["permanent_url"])
            if not url:
                raise Exception("Channel not on Live!!!")
            return url
        except Exception as e:
            log_error(str(e))
            return False

    def write_json(self, data: dict, name: str = "data.json") -> bool:
        try:
            with open(name, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            log_error(str(e))
            return False

    def read_json(self, name: str = "data.json") -> dict:
        try:
            with open(name) as json_file:
                return json.load(json_file)
        except Exception as e:
            log_error(str(e))
            return {}

    def get_video_id(self, url: str) -> str:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html5lib")
                murl = soup.find("link", {"rel": "canonical"})
                return murl["href"]
        except Exception as e:
            log_error(str(e))
            return ""

    def pause(self):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def reload_video(self):
        raise NotImplementedError


class MPVPlayer(Player, threading.Thread):
    def __init__(self, mode=0, video="./songs/Minecraft_Sweden.mp3"):
        super().__init__()
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self.player = mpv.MPV(
            video=False, ytdl=True, cache=False, cache_secs=1, pause=True, 
            ytdl_format="bestaudio/best", log_handler=log_MPV_message
        )
        self.url = self.get_video_stream()
        self.mode = mode
        self.video = video
        self.player._set_property("volume", 100)
        self.playing = False
        self.muted = False

        # Attach event listener for errors and stream end
        @self.player.event_callback("end-file")
        def on_end_file(event):
            self.reconnect()

    def run(self):
        self.state = 1
        self.start_playback()

    def start_playback(self):
        try:
            if self.mode == 0:
                self.url = self.get_video_stream()
                if self.url:
                    print(f"Starting stream: {self.url}")
                    self.player.play(self.url)
                else:
                    raise Exception("Problem fetching URL")
            else:
                self.player.loop = True
                self.player.play(self.video)
        except Exception as e:
            log_error(f"Playback start failed: {e}")
            time.sleep(5)
            self.reconnect()

    def reconnect(self):
        """Reconnect to stream after error/end."""
        if not self.stopped.is_set():
            log_error("Attempting to reconnect...")
            time.sleep(2)  # short delay before retry
            self.start_playback()

    def change_mode(self, mode):
        try:
            self.mode = mode
            return True
        except Exception as e:
            log_error(str(e))
            return False

    def change_video(self, video):
        try:
            self.video = video
            return True
        except Exception as e:
            log_error(str(e))
            return False

    def toggle_play(self):
        self.playing = not self.playing
        self.player.pause = not self.player.pause

    def toggle_mute(self):
        if self.muted:
            self.player._set_property("volume", 100)
        else:
            self.player._set_property("volume", 0)
        self.muted = not self.muted

    def pause(self):
        self.state = 2
        self.player.pause = True

    def play(self):
        self.state = 1
        self.player.pause = False

    def stop(self):
        self.state = 0
        self.stopped.set()
        if self.player:
            self.player.terminate()

    def main(self):
        self.start()
        return True



class WNMPlayer(Player, threading.Thread):
    def __init__(self, video="./songs/Minecraft_Sweden.mp3"):
        super().__init__()
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        self.player = mpv.MPV(video=False, cache=True, cache_secs=1, pause=True)
        self.url = self.get_video_stream()
        self.video = video
        self.player._set_property("volume", 100)
        self.playing = False
        self.muted = False

    def run(self):
        self.state = 1
        self.player.loop = True
        self.player.play(self.video)
        self.player.wait_until_playing()

    def change_video(self, video):
        try:
            self.video = video
            return True
        except Exception as e:
            print(e)
            return False

    def toggle_play(self):
        self.playing = not self.playing
        self.player.pause = not self.player.pause

    def toggle_mute(self):
        if self.muted:
            self.player._set_property("volume", 100)
        else:
            self.player._set_property("volume", 0)
        self.muted = not self.muted

    def pause(self):
        self.state = 2
        self.player.pause = True

    def play(self):
        self.state = 1
        self.player.pause = False

    def stop(self):
        self.state = 0
        self.stopped.set()
        if self.player:
            self.player.terminate()

    def main(self):
        self.start()
        return True
