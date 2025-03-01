Get-Playlist is a barebones application made with Flask to get playlist contents from YouTube. This was my first time using Flask, and creating a server to manage the backend.
app2.py contains the code that Render, the backend server deploys, which creates the live link https://youtube-playlist-getter.onrender.com
From there, there are two endpoints which are /get_channel_playlists and /get_playlist_videos.
The user can then run the client.py, which prompts them for channel input and grabs the data through google-api-python-client.

<img width="443" alt="Image" src="https://github.com/user-attachments/assets/4e1c6e8a-2645-46b4-be6e-e4d45d72ea70" />
<img width="191" alt="Image" src="https://github.com/user-attachments/assets/f68e3efd-f856-48b9-a9df-c349d3a5045b" />
<img width="280" alt="Screenshot 2025-03-01 at 3 24 49 PM" src="https://github.com/user-attachments/assets/e93cd62a-3bba-4f9e-a02b-f113802cb2e8" />


Requirements for this project:
flask,
requests,
python-dotenv,
google-api-python-client,
gunicorn (for Render)
