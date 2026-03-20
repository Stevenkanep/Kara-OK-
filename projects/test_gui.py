# test_gui.py
import tkinter as tk
from tkinter import messagebox
import service

# Initialize backend (loads songs and queue from data files)
service.init_backend()

# --- Remote / Keypad helper (integrated) ---
def create_remote(parent_frame, refresh_callback):
    """
    Create a simple keypad remote inside parent_frame.
    refresh_callback: function to call after queue changes (e.g., refresh_queue_display)
    Returns the Entry widget used for the song ID.
    """
    remote_frame = tk.Frame(parent_frame)
    remote_frame.pack(padx=6, pady=4, anchor="w")

    # Display / entry for the song ID
    tk.Label(remote_frame, text="Song ID:").grid(row=0, column=0, columnspan=3, sticky="w")
    entry_id = tk.Entry(remote_frame, width=12, justify="center")
    entry_id.grid(row=1, column=0, columnspan=3, pady=(0,6))

    # Digit button handlers
    def on_digit(d):
        entry_id.insert(tk.END, str(d))

    def on_backspace():
        cur = entry_id.get()
        entry_id.delete(0, tk.END)
        entry_id.insert(0, cur[:-1])

    def on_clear():
        entry_id.delete(0, tk.END)

    def on_add():
        sid = entry_id.get().strip()
        if not sid:
            messagebox.showwarning("Input", "Enter a song ID")
            return
        try:
            service.reserve_song(sid)
            refresh_callback()
            entry_id.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # keypad layout (3x4)
    digits = [
        ('1', 0, 2), ('2', 1, 2), ('3', 2, 2),
        ('4', 0, 3), ('5', 1, 3), ('6', 2, 3),
        ('7', 0, 4), ('8', 1, 4), ('9', 2, 4),
        ('Clear', 0, 5), ('0', 1, 5), ('⌫', 2, 5),
    ]

    for (label, col, row) in digits:
        if label == 'Clear':
            btn = tk.Button(remote_frame, text=label, width=6, command=on_clear)
        elif label == '⌫':
            btn = tk.Button(remote_frame, text=label, width=6, command=on_backspace)
        else:
            btn = tk.Button(remote_frame, text=label, width=6, command=lambda d=label: on_digit(d))
        btn.grid(row=row, column=col, padx=2, pady=2)

    # Add and Skip buttons below keypad
    btn_add = tk.Button(remote_frame, text="Add", width=8, command=on_add)
    btn_add.grid(row=6, column=0, columnspan=2, pady=(6,0), sticky="w")

    btn_skip = tk.Button(remote_frame, text="Skip Current", width=12,
                         command=lambda: (service.skip_current(), refresh_callback()))
    btn_skip.grid(row=6, column=2, pady=(6,0), sticky="e")

    return entry_id

# --- GUI functions ---
def refresh_queue_display():
    q = service.get_queue()
    listbox_queue.delete(0, tk.END)
    for sid in q:
        info = service._songs.get(sid, {})
        title = info.get('title', 'Unknown')
        listbox_queue.insert(tk.END, f"{sid} | {title}")
    current = service.current_song()
    if current:
        label_current.config(text=f"Now Playing: {current.get('id')} | {current.get('title')}")
    else:
        label_current.config(text="Now Playing: (none)")

def search_action():
    q = entry_search.get().strip()
    results = service.search_songs(q) if q else service.get_all_songs()
    listbox_songs.delete(0, tk.END)
    for s in results:
        listbox_songs.insert(tk.END, f"{s['id']} | {s['title']} - {s['artist']}")

# --- Build main window ---
root = tk.Tk()
root.title("Kara-OK!")

# Home frame
frame_home = tk.LabelFrame(root, text="Home")
frame_home.pack(fill="x", padx=8, pady=6)

label_current = tk.Label(frame_home, text="Now Playing: (none)")
label_current.pack(anchor="w", padx=6, pady=4)

tk.Label(frame_home, text="Queue:").pack(anchor="w", padx=6)
listbox_queue = tk.Listbox(frame_home, width=60, height=6)
listbox_queue.pack(padx=6, pady=4)

# Insert keypad remote into Home frame
entry_remote = create_remote(frame_home, refresh_queue_display)

# SongBook frame
frame_songbook = tk.LabelFrame(root, text="SongBook")
frame_songbook.pack(fill="both", expand=True, padx=8, pady=6)

search_frame = tk.Frame(frame_songbook)
search_frame.pack(fill="x", padx=6, pady=4)
entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side="left")
tk.Button(search_frame, text="Search", command=search_action).pack(side="left", padx=4)
tk.Button(search_frame, text="Show All", command=search_action).pack(side="left", padx=4)

listbox_songs = tk.Listbox(frame_songbook, width=80, height=10)
listbox_songs.pack(padx=6, pady=4)

# initial populate
search_action()
refresh_queue_display()

root.mainloop()
