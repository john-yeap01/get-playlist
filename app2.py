from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

@app.route('/get_channel_playlists', methods=['GET'])
def get_channel_playlists():
    """
    Endpoint that retrieves channel playlists.
    Accepts a query parameter "channel" that can be either a channel ID or a handle (starting with '@').
    """
    user_input = request.args.get('channel')
    if not user_input:
        return jsonify({'error': 'channel parameter is required'}), 400

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # If the input starts with '@', assume it's a handle and convert it to a channel ID.
    if user_input.startswith('@'):
        channel_req = youtube.channels().list(
            part="id",
            forHandle=user_input  # Pass the handle as provided (e.g., "@SomeHandle")
        )
        channel_resp = channel_req.execute()
        items = channel_resp.get("items", [])
        if not items:
            return jsonify({'error': 'No channel found for the provided handle'}), 404
        channel_id = items[0]["id"]
    else:
        # Otherwise, assume the input is already a channel ID.
        channel_id = user_input

    # Now fetch the playlists for the channel ID.
    youtube_url = "https://www.googleapis.com/youtube/v3/playlists"
    params = {
        'part': 'snippet,contentDetails',
        'channelId': channel_id,
        'maxResults': 50,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(youtube_url, params=params)
    return jsonify(response.json())

@app.route('/get_playlist_videos', methods=['GET'])
def get_playlist_videos():
    """
    Endpoint that retrieves videos from a specific playlist.
    Expects a query parameter "playlist" (the playlist ID).
    """
    playlist_id = request.args.get('playlist')
    if not playlist_id:
        return jsonify({'error': 'playlist parameter is required'}), 400

    youtube_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet,contentDetails',
        'playlistId': playlist_id,
        'maxResults': 50,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(youtube_url, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
