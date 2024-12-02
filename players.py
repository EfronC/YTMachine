import threading
import json
import requests
from bs4 import BeautifulSoup
import mpv

class Player:
	def __init__(self):
		self.state = 0  # 0 - stopped, 1 - playing, 2 - paused
		self.player = None
		self.url = None

	def update_permanent_url(self, url: str):
		try:
			data = self.read_json("data.json")
			data["permanent_url"] = url
			self.write_json(data, "data.json")
			return True
		except Exception as e:
			print(e)
			return False

	def get_video_stream(self):
		try:
			data = self.read_json("data.json")
			url = data.get("video_url", False)
			if not url:
				print("Not an URL. Getting real URL...")
				url = self.get_video_id(data["permanent_url"])
				if url:
					data["video_url"] = url
					self.write_json(data, "data.json")
				else:
					data["video_url"] = ""
					self.write_json(data, "data.json")
					raise Exception("Channel not on Live!!!")
			return url
		except Exception as e:
			print(e)
			return False

	def write_json(self, data: dict, name: str = "data.json") -> bool:
		try:
			with open(name, 'w', encoding='utf-8') as outfile:
				json.dump(data, outfile, ensure_ascii=False, indent=4)
			return True
		except Exception as e:
			print(e)
			return False

	def read_json(self, name: str = "data.json") -> dict:
		try:
			with open(name) as json_file:
				return json.load(json_file)
		except Exception as e:
			print(e)
			return {}

	def get_video_id(self, url: str) -> str:
		try:
			r = requests.get(url)
			if r.status_code == 200:
				soup = BeautifulSoup(r.content, "html5lib")
				murl = soup.find("link", {"rel": "canonical"})
				return murl["href"]
		except Exception as e:
			print(e)
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
	def __init__(self):
		super().__init__()
		threading.Thread.__init__(self)
		self.stopped = threading.Event()
		self.player = mpv.MPV(video=False, ytdl=True)
		self.url = self.get_video_stream()

	def run(self):
		self.state = 1
		self.player.play(self.url)
		self.player.wait_for_playback()

	def reload_video(self):
		try:
			print("Reloading video...")
			playurl = self.get_video_stream()
			self.url = playurl
			if playurl:
				self.player.play(self.url)
				self.player.wait_for_playback()
				return True
			return False
		except Exception as e:
			print(e)
			return False

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
