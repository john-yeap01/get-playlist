from googleapiclient.discovery import build
import re
import tkinter as tk

api_key = 'AIzaSyAXRqBuKMvXTpi8kbsg_up8E1fxNXOheBI'
youtube =  build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part = 'contentDetails, statistics',
    forHandle='johnyeap7133'
)

response = request.execute()
channel_id = response['items'][0]['id']

pl_request = youtube.playlists().list(
    part = 'snippet',
    channelId = channel_id
)
pl_response = pl_request.execute()
print(pl_response)


playlist_id = pl_response['items'][0]['id']

vid_request = youtube.playlistItems().list(
    part = 'snippet, contentDetails',
    playlistId = playlist_id,
    maxResults=50
)

all_videos = []


vid_response = vid_request.execute()
videos = vid_response.get('items', [])
all_videos.extend(videos)


for video in all_videos:
    print(video)
    title = video['snippet']['title']
    print(title)

# for item in vid_response['items']:
#     title = item['contentDetails']['videoId']
#     print(item)
#     print(title)

# for item in pl_response['items']:
#     print(item['snippet']['title'])
#     print()

# print(pl_response['items'][0]['id'])



def get_all_playlist_videos(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)

    all_videos = []
    next_page_token = None

    while True:
        vid_request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,  # The max allowed per request
            pageToken=next_page_token
        )
        vid_response = vid_request.execute()

        # Append the items from this page
        items = vid_response.get("items", [])
        all_videos.extend(items) # add to the list after each page

        # Check if there's another page
        # make the next page token the new page token
        next_page_token = vid_response.get("nextPageToken")
        if not next_page_token:
            break

    return all_videos

if __name__ == "__main__":
    

    # Get channel ID from handle (johnyeap7133)
    youtube = build("youtube", "v3", developerKey=api_key)
    channel_req = youtube.channels().list(
        part="contentDetails,statistics",
        forHandle="johnyeap7133"
    )
    channel_resp = channel_req.execute()
    channel_id = channel_resp["items"][0]["id"]

    # Get a playlist ID from that channel (you might need a loop to find the specific one you want)
    pl_request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    )
    pl_response = pl_request.execute()
    # For demonstration, just take the first playlist
    playlist_id = pl_response["items"][2]["id"]

    # Fetch *all* videos from that playlist
    videos = get_all_playlist_videos(api_key, playlist_id)

    counter = 0
    # Print out the titles
    for vid in videos:
        snippet = vid.get("snippet", {})
        title = snippet.get("title", "Unknown title")
        # print(title)
        counter += 1

    print('___________')
    print("PLAYLISTS")
    for item in pl_response['items']:
        print(item['snippet']['title'])
        print()
    print(counter)


    print(vid_response)
