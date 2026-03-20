# storage.py
import json
from typing import Dict, List

USERS_FILE = "data/users.json"
SONGS_FILE = "data/songs.json"
QUEUE_FILE = "data/queue.json"

def load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception:
        raise

def save_json(path: str, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        raise

def load_songs() -> Dict[str, Dict]:
    return load_json(SONGS_FILE, {})

def save_songs(songs: Dict[str, Dict]):
    save_json(SONGS_FILE, songs)

def load_queue() -> List[str]:
    return load_json(QUEUE_FILE, [])

def save_queue(queue_list: List[str]):
    save_json(QUEUE_FILE, queue_list)
