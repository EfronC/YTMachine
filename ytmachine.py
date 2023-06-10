import time
from threading import Event
import signal
import ujson as json

import pafy
import vlc
import requests
from bs4 import BeautifulSoup

class LiveStreamPlayer:
	def __init__(self):
		self.state = 3 # 0 - stopped, 1 - playing, 2 - paused
		self.player = None
		self.Instance = None

	def prepare_video_data(self):
		try:
			print("Reloading video...")
			data = self.read_json("data.json")
			url = False
			if data["video_url"]:
				print("Found url")
				url = data["video_url"]
			else:
				print("Not an URL")
				print("Getting real url...")
				url = self.get_video_id(data["permanent_url"])
				if url:
					data["video_url"] = url
					self.write_json(data, "data.json")
				else:
					data["video_url"] = ""
					self.write_json(data, "data.json")
					raise Exception("Channel not on Live!!!")
			print("URL found:", url)
			print("Getting Best URL...")
			playurl = self.get_video(url)
			if not playurl:
				print("Getting real url...")
				url = self.get_video_id(data["permanent_url"])
				if url:
					data["video_url"] = url
					self.write_json(data, "data.json")
					playurl = self.get_video(url)
				else:
					data["video_url"] = ""
					self.write_json(data, "data.json")
					raise Exception("Channel not on Live!!!")

			if playurl:
				Media = self.Instance.media_new(playurl)
				Media.get_mrl()
				self.player.set_media(Media)
				print("Player ready!")
				return True
			return False
		except Exception as e:
			print(e)
			return False

	def pause(self):
		self.state = 2
		self.player.pause()

	def play(self):
		if self.state == 0:
			playurl = self.prepare_video_data()
		self.state = 1
		self.player.play()

	def stop(self):
		self.state = 0
		self.player.stop()

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
			data = []
			with open(name) as json_file:
				data = json.load(json_file)
			return data
		except Exception as e:
			print(e)
			return []

	def get_video(self, url: str) -> str:
		try:
			video = pafy.new(url)
			best = video.getbest()
			playurl = best.url
			#print(playurl)
			return playurl
		except Exception as e:
			print(e)
			return False

	def get_video_id(self, url: str) -> str:
		r = requests.get(url)
		if int(r.status_code) == 200:
			soup = BeautifulSoup(r.content, "html5lib")
			murl = soup.find("link", {"rel":"canonical"})
			return murl["href"]
		else:
			pass

	def main(self) -> bool:
		try:
			data = self.read_json("data.json")
			url = False
			if data["video_url"]:
				print("Found url")
				url = data["video_url"]
			else:
				print("Not an URL")
				print("Getting real url...")
				url = self.get_video_id(data["permanent_url"])
				if url:
					data["video_url"] = url
					self.write_json(data, "data.json")
				else:
					data["video_url"] = ""
					self.write_json(data, "data.json")
					raise Exception("Channel not on Live!!!")
			print("URL found:", url)
			print("Getting Best URL...")
			playurl = self.get_video(url)
			if not playurl:
				print("Getting real url...")
				url = self.get_video_id(data["permanent_url"])
				if url:
					data["video_url"] = url
					self.write_json(data, "data.json")
					playurl = self.get_video(url)
				else:
					data["video_url"] = ""
					self.write_json(data, "data.json")
					raise Exception("Channel not on Live!!!")

			if playurl:
				print("Best URL found!")
				print("Starting VLC...")
				self.Instance = vlc.Instance('--no-video')
				self.player = self.Instance.media_player_new()
				Media = self.Instance.media_new(playurl)
				Media.get_mrl()
				self.player.set_media(Media)
				print("Player ready!")
				return True
			return False
		except Exception as e:
			print(e)
			return False
