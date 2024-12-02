# import mpv
# import time
# import threading

# class YTPlayer(mpv.MPV):

# 	def __init__(self, *args, **kwargs):
# 		# Pass a window id to embed mpv into that window. Change debug to True
# 		# to see the json communication.
# 		super().__init__(*args, **kwargs)


# player = YTPlayer(ytdl=True, video=False)
# player.play('https://www.youtube.com/c/henrikomagnifico/live')
# x = player.wait_for_playback()


# import threading
# import mpv
# import time

# class PlayerThread(threading.Thread):
#     def __init__(self, url):
#         super(PlayerThread, self).__init__()
#         self.player = mpv.MPV(video=False, ytdl=True)
#         self.url = url
#         self.playing = False
#         self.stopped = threading.Event()

#     def run(self):
#         self.player.play(self.url)
#         self.player.wait_for_playback()

#     def toggle_play(self):
#         self.playing = not self.playing
#         self.player.pause = not self.player.pause

#     def stop(self):
#         self.stopped.set()
#         self.player.terminate()

# # YouTube URL to play
# youtube_url = "https://www.youtube.com/c/henrikomagnifico/live"

# # Create an instance of PlayerThread
# player_thread = PlayerThread(youtube_url)
# player_thread.start()

# # Function to send play/pause command to the player thread
# def send_play_pause_command():
#     player_thread.toggle_play()

# # Function to stop the player thread
# def stop_player_thread():
#     player_thread.stop()

# # Example: Send play/pause command
# #send_play_pause_command()

# time.sleep(10)
# send_play_pause_command()
# time.sleep(10)
# send_play_pause_command()
# time.sleep(10)
# stop_player_thread()

from players import MPVPlayer
import time

player = MPVPlayer()
print("Play")
player.main()
print("Sleep")
time.sleep(20)
# print("Reloading")
# player.reload_video()
# print("Sleep")
# time.sleep(20)
print("Stopping")
player.stop()
print("Sleep")
time.sleep(10)
print("Play")
player.main()
print("Sleep")
time.sleep(20)
print("Stopping")
player.stop()
