import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path


class Repository:
    def __init__(self, profile):
        folder = Path(profile) / 'incremental_reading'
        folder.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(folder / 'reading.sqlite3')
        self.db.row_factory = sqlite3.Row
        version = self.db.execute('PRAGMA user_version').fetchone()[0]
        if version > 1:
            self.db.close()
            raise ValueError('Reading database requires a newer add-on')
        if version == 0:
            with self.db:
                self.db.execute('CREATE TABLE topics (id TEXT PRIMARY KEY, source_id TEXT UNIQUE NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, citation TEXT NOT NULL, position TEXT NOT NULL DEFAULT \'{}\', created TEXT NOT NULL, opened TEXT NOT NULL)')
                self.db.execute('PRAGMA user_version=1')

    def add(self, title, content, citation=''):
        if not title.strip() or not content.strip():
            raise ValueError('Title and text are required')
        key = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        with self.db:
            self.db.execute('INSERT INTO topics VALUES (?,?,?,?,?,?,?,?)', (key, str(uuid.uuid4()), title.strip(), content, citation, '{}', now, now))
        return key

    def search(self, query=''):
        return [dict(r) for r in self.db.execute('SELECT * FROM topics ORDER BY opened DESC, id') if query.casefold() in (r['title'] + '\n' + r['content']).casefold()]

    def get(self, key):
        row = self.db.execute('SELECT * FROM topics WHERE id=?', (key,)).fetchone()
        if row is None:
            raise ValueError('Unknown topic')
        return dict(row)

    def opened(self, key):
        with self.db:
            self.db.execute('UPDATE topics SET opened=? WHERE id=?', (datetime.now(timezone.utc).isoformat(), key))

    def save(self, key, position):
        if set(position) != {'paragraph', 'fraction'} or type(position['paragraph']) is not int or position['paragraph'] < 0 or type(position['fraction']) not in (int, float) or not 0 <= position['fraction'] <= 1:
            raise ValueError('Invalid reading position')
        with self.db:
            self.db.execute('UPDATE topics SET position=? WHERE id=?', (json.dumps(position), key))

    def close(self):
        self.db.close()
