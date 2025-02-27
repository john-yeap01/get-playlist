import re
import sys
import tkinter as tk
from tkinter import simpledialog
from googleapiclient.discovery import build

API_KEY = "AIzaSyAXRqBuKMvXTpi8kbsg_up8E1fxNXOheBI"

def parse_channel_info(youtube_url: str):
    """
    Attempt to parse the channel 'handle' or 'channelId' from a given YouTube URL.
    Returns a dict like {"handle": "..."} or {"channel_id": "..."} or None if parsing fails.
    """
    # Check for an "@handle" style link, e.g. youtube.com/@SomeHandle
    handle_match = re.search(r'youtube\.com/@([\w\-]+)', youtube_url)
    if handle_match:
        return {"handle": handle_match.group(1)}

    # Check for a "/channel/UCxxxx" style link, e.g. youtube.com/channel/UCxxxxxxx
    chan_id_match = re.search(r'youtube\.com/channel/([\w\-]+)', youtube_url)
    if chan_id_match:
        return {"channel_id": chan_id_match.group(1)}

    # If neither pattern matched, return None
    return None


def get_all_channel_playlists(api_key, channel_id):
    """
    Retrieve all the playlists owned by a channel, paging through results if necessary.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    all_playlists = []
    next_page_token = None

    while True:
        pl_request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        
        all_playlists.extend(pl_response.get("items", []))
        
        next_page_token = pl_response.get("nextPageToken")
        if not next_page_token:
            break

    return all_playlists


def get_all_playlist_videos(api_key, playlist_id):
    """
    Retrieve all the videos from a given playlist by paging through results.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    all_videos = []
    next_page_token = None

    while True:
        vid_request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        vid_response = vid_request.execute()

        items = vid_response.get("items", [])
        all_videos.extend(items)

        next_page_token = vid_response.get("nextPageToken")
        if not next_page_token:
            break

    return all_videos


def choose_playlist(playlists):
    """
    Present a Tkinter Listbox of all playlists, allowing the user to select one.
    Returns the ID of the chosen playlist, or None if none selected.
    """
    root = tk.Tk()
    root.title("Select a Playlist")

    selected_playlist_id = None

    # Create a Listbox to display playlist titles
    lb = tk.Listbox(root, width=70, height=10)
    lb.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Insert each playlist title into the listbox
    for i, pl in enumerate(playlists):
        pl_title = pl["snippet"]["title"]
        lb.insert(tk.END, f"{i+1}. {pl_title}")

    def on_select():
        nonlocal selected_playlist_id
        selection = lb.curselection()
        if selection:
            index = selection[0]
            selected_playlist_id = playlists[index]["id"]
        root.destroy()

    # OK button to confirm selection
    btn = tk.Button(root, text="OK", command=on_select)
    btn.pack(pady=5)

    root.mainloop()
    return selected_playlist_id


def show_playlist_videos(videos):
    """
    Display a Tkinter window listing video titles in the chosen playlist.
    """
    root = tk.Tk()
    root.title("Playlist Videos")

    lb = tk.Listbox(root, width=80, height=20)
    lb.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for v in videos:
        vid_title = v["snippet"]["title"]
        lb.insert(tk.END, vid_title)

    # A close button to close the video list window
    btn_close = tk.Button(root, text="Close", command=root.destroy)
    btn_close.pack(pady=5)

    root.mainloop()


def list_channel_playlists(api_key, youtube_url):
    """
    1. Determine if it's a channel 'handle' or channel 'id'.
    2. Get the channel details.
    3. List all playlists in that channel.
    4. Ask the user (in a Tkinter listbox) to select one playlist.
    5. Show all videos from that selected playlist in another Tkinter listbox.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # Parse the URL for a handle or channel ID
    channel_info = parse_channel_info(youtube_url)
    if channel_info is None:
        print("Could not parse the YouTube channel link. Please provide a link like:")
        print("  https://youtube.com/@SomeHandle  OR  https://youtube.com/channel/UCxxxxxxx")
        sys.exit(1)

    # Build our channels().list request
    if "handle" in channel_info:
        channel_req = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forHandle=channel_info["handle"]
        )
    else:
        channel_req = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_info["channel_id"]
        )
    
    channel_resp = channel_req.execute()
    items = channel_resp.get("items", [])
    if not items:
        print("No channel found with that link.")
        sys.exit(1)

    channel_id = items[0]["id"]
    channel_title = items[0]["snippet"]["title"]

    # Retrieve the playlists owned by the channel
    all_playlists = get_all_channel_playlists(api_key, channel_id)
    print(f"Found {len(all_playlists)} playlists for channel '{channel_title}'")

    if not all_playlists:
        print("This channel has no public playlists.")
        return

    # Let the user select a playlist
    chosen_id = choose_playlist(all_playlists)
    if chosen_id:
        # Retrieve the videos for that chosen playlist
        videos = get_all_playlist_videos(api_key, chosen_id)
        print(f"Playlist has {len(videos)} videos. Opening UI to show them...")
        show_playlist_videos(videos)
    else:
        print("No playlist was chosen.")


def ask_for_youtube_link():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    link = simpledialog.askstring("YouTube Link", "Enter the YouTuber's channel link:")
    root.destroy()
    return link


if __name__ == "__main__":
    youtube_url = ask_for_youtube_link()
    if youtube_url:
        list_channel_playlists(API_KEY, youtube_url)
    else:
        print("No link entered.")

    
