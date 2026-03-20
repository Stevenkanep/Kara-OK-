# service.py
from models import Song
import storage
import random

_songs = {}   # id -> dict
_queue = []   # list of song ids

def init_backend():
    global _songs, _queue
    _songs = storage.load_songs()
    _queue = storage.load_queue()

# SongBook functions
def get_all_songs():
    return list(_songs.values())

def search_songs(query: str):
    q = query.lower().strip()
    results = []
    for sid, info in _songs.items():
        if q in sid.lower() or q in info.get("title","").lower() or q in info.get("artist","").lower():
            results.append(info)
    return results

def add_song_to_catalog(sid: str, title: str, artist: str, lyrics: str = ""):
    _songs[sid] = {"id": sid, "title": title, "artist": artist, "lyrics": lyrics}
    storage.save_songs(_songs)

# Queue functions (Home page remote)
def reserve_song(song_id: str):
    if song_id not in _songs:
        raise ValueError("Song ID not found")
    _queue.append(song_id)
    storage.save_queue(_queue)

def get_queue():
    return list(_queue)

def current_song():
    return _songs.get(_queue[0]) if _queue else None

def skip_current():
    if _queue:
        skipped = _queue.pop(0)
        storage.save_queue(_queue)
        return skipped
    return None

# Simple scoring placeholder
def score_performance(song_id: str, performance_text: str = "") -> int:
    lyrics = _songs.get(song_id, {}).get("lyrics", "")
    base = len(lyrics) % 70
    rand = random.randint(0, 30)
    return min(100, base + rand)
