# models.py
class Song:
    def __init__(self, sid: str, title: str, artist: str, lyrics: str = ""):
        self.id = sid
        self.title = title
        self.artist = artist
        self.lyrics = lyrics

    def to_dict(self):
        return {"id": self.id, "title": self.title, "artist": self.artist, "lyrics": self.lyrics}

    @staticmethod
    def from_dict(d):
        return Song(d["id"], d["title"], d["artist"], d.get("lyrics", ""))
