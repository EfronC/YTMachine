# YoutubeMachine

Flask app to connect to a Stream on YT.

## Requirements
- BeautifulSoup4
- Requests
- Pafy
- Youtube_dl
- VLC

Note: Pafy needs to be modified manually by commenting/updating a few lines for this to work, by commenting these lines on backend_youtube_dl.py

```
self._likes = self._ydl_info['like_count']
self._dislikes = self._ydl_info['dislike_count']
```

And in youtube_dl, in youtube_dl/extractor/youtube.py, change this line

```
'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id') if owner_profile_url else None
```

for

``` 
'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id', fatal=False) if owner_profile_url else None
```

## Usage

- Fill the field "permanent_url" in the data.json with the permanent Live URL to the channel wished. ex:`https://www.youtube.com/c/<USERNAME>/live`.
- Load the flask app with `flask run -h 0.0.0.0 --no-reload` for a testing server in a local network scenario, or configure a server for the app. 
- You can interact with the player with a GET request to `http://<local_server_ip:port>/<instruction>`, with instruction being one of play/pause/stop.