Get-Playlist is a barebones application made with Flask to get playlist contents from YouTube. This was my first time using Flask, and creating a server to manage the backend.
app2.py contains the code that Render, the backend server deploys, which creates the live link https://youtube-playlist-getter.onrender.com
From there, there are two endpoints which are /get_channel_playlists and /get_playlist_videos.
The user can then run the client.py, which prompts them for channel input and grabs the data through google-api-python-client.



Requirements for this project:
flask,
requests,
python-dotenv,
google-api-python-client,
gunicorn (for Render)
