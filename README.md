# YoutubeMachine

Flask app to connect to a Stream on YT.

## Requirements
- Docker
- Docker compose

## Usage

- Fill the field "permanent_url" in the data.json with the permanent Live URL to the channel wished. ex:`https://www.youtube.com/c/<USERNAME>/live`.
- For the WNM: Create a folder "songs" and add your mp3.
- Start the application with `docker compose build && docker compose up -d`