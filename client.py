import tkinter as tk
from tkinter import simpledialog, messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  # The URL where your Flask backend is running

def ask_for_channel():
    """
    Pops up a dialog asking the user for a channel handle or ID.
    Returns the string input, or None if cancelled.
    """
    root = tk.Tk()
    root.withdraw()  # Hide main window

    user_input = simpledialog.askstring(
        title="YouTube Channel",
        prompt="Enter a YouTube channel handle (e.g., @SomeHandle) or channel ID:"
    )
    root.destroy()
    return user_input

def fetch_playlists(channel):
    """
    Calls the Flask backend to fetch playlists for the given channel (handle or ID).
    Returns the JSON data or None if there's an error.
    """
    url = f"{BASE_URL}/get_channel_playlists"
    params = {"channel": channel}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch playlists:\n{e}")
        return None

def fetch_videos(playlist_id):
    """
    Calls the Flask backend to fetch videos for the given playlist ID.
    Returns the JSON data or None if there's an error.
    """
    url = f"{BASE_URL}/get_playlist_videos"
    params = {"playlist": playlist_id}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch videos:\n{e}")
        return None

def choose_playlist_window(playlists):
    """
    Displays a Tkinter window with a Listbox of all playlists.
    Returns the selected playlist ID or None if nothing selected.
    """
    if "items" not in playlists:
        messagebox.showerror("Error", "No valid data returned for playlists.")
        return None
    
    items = playlists["items"]
    if not items:
        messagebox.showinfo("No Playlists", "No playlists found for this channel.")
        return None

    root = tk.Tk()
    root.title("Select a Playlist")
    root.geometry("500x300")

    lb = tk.Listbox(root, width=60, height=10)
    lb.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Populate the listbox with playlist titles
    for i, pl in enumerate(items):
        pl_title = pl["snippet"]["title"]
        pl_id = pl["id"]
        lb.insert(tk.END, f"{pl_title} (ID: {pl_id})")

    selected_playlist_id = tk.StringVar()

    def on_select():
        sel_index = lb.curselection()
        if sel_index:
            # Grab the corresponding playlist ID from items
            idx = sel_index[0]
            selected_playlist_id.set(items[idx]["id"])
        root.destroy()

    btn_ok = tk.Button(root, text="OK", command=on_select)
    btn_ok.pack(pady=5)

    root.mainloop()

    return selected_playlist_id.get() or None

def show_videos_window(videos_json):
    """
    Displays a new Tkinter window listing video titles from the JSON response.
    """
    if "items" not in videos_json:
        messagebox.showerror("Error", "No valid data returned for videos.")
        return
    
    items = videos_json["items"]
    if not items:
        messagebox.showinfo("No Videos", "No videos found in this playlist.")
        return

    root = tk.Tk()
    root.title("Playlist Videos")
    root.geometry("600x400")

    lb = tk.Listbox(root, width=80, height=15)
    lb.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for video_item in items:
        snippet = video_item["snippet"]
        title = snippet["title"]
        lb.insert(tk.END, title)

    btn_close = tk.Button(root, text="Close", command=root.destroy)
    btn_close.pack(pady=5)

    root.mainloop()

def main():
    channel = ask_for_channel()
    if not channel:
        return  # user cancelled

    playlists_data = fetch_playlists(channel)
    if not playlists_data:
        return  # error or no data

    chosen_playlist_id = choose_playlist_window(playlists_data)
    if not chosen_playlist_id:
        return  # user cancelled or no playlist chosen

    videos_data = fetch_videos(chosen_playlist_id)
    if videos_data:
        show_videos_window(videos_data)

if __name__ == "__main__":
    main()
