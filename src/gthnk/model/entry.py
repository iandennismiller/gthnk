import os


class Entry(object):
    def __init__(self, day, timestamp, content=None):
        self.day = day
        self.timestamp = timestamp
        self.content = content
    
    def get_uri(self):
        return os.path.join(self.day.journal.get_uri(), self.day.day_id, f"{self.timestamp}.txt")

    def render_standalone(self):
        return f"{self.day.day_id}\n\n{self.timestamp}\n\n{self.content}\n"

    def __repr__(self):
        return f"{self.timestamp}\n\n{self.content}\n\n"
