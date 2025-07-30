import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Dict

from .config import get_settings

# _CREATE_SQL = """
# CREATE TABLE IF NOT EXISTS completions (
#     id TEXT PRIMARY KEY,
#     prompt TEXT,
#     response TEXT
# );
# """


# class Cache:
#     """
#     Tiny SQLite cache (prompt → response). Fully optional.
#     """

#     def __init__(self) -> None:
#         cfg = get_settings()
#         self.path: Path = cfg.cache_path
#         self._enable = cfg.enable_cache
#         if self._enable:
#             with closing(sqlite3.connect(self.path)) as conn:
#                 conn.execute(_CREATE_SQL)
#                 conn.commit()

#     @staticmethod
#     def _prompt_hash(prompt: str) -> str:
#         return hashlib.sha256(prompt.encode()).hexdigest()

#     def get(self, prompt: str) -> str | None:
#         if not self._enable:
#             return None
#         h = self._prompt_hash(prompt)
#         with closing(sqlite3.connect(self.path)) as conn:
#             cur = conn.execute(
#                 "SELECT response FROM completions WHERE id = ?;", (h,)
#             )
#             row = cur.fetchone()
#             return row[0] if row else None

#     def set(self, prompt: str, response: str) -> None:
#         if not self._enable:
#             return
#         h = self._prompt_hash(prompt)
#         with closing(sqlite3.connect(self.path)) as conn:
#             conn.execute(
#                 "INSERT OR REPLACE INTO completions (id, prompt, response) "
#                 "VALUES (?, ?, ?);",
#                 (h, prompt, response),
#             )
#             conn.commit()

import redis
import os
import hashlib

def get_redis_client():
    host = os.getenv('REDIS_HOST', 'localhost')
    port = int(os.getenv('REDIS_PORT', 6379))
    db = int(os.getenv('REDIS_DB', 0))
    password = os.getenv('REDIS_PASSWORD')
    return redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)

class Cache:
    def __init__(self):
        self.r = get_redis_client()

    @staticmethod
    def _prompt_hash(prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str) -> str | None:
        h = self._prompt_hash(prompt)
        return self.r.get(h)

    def set(self, prompt: str, response: str) -> None:
        h = self._prompt_hash(prompt)
        self.r.set(h, response, ex=60*60*24)  # expire in 24h