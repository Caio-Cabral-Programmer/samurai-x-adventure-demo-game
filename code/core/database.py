"""SQLite database for persistent score storage."""

import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    """Manages player names and score records in a local SQLite database."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._initialize()

    def _initialize(self) -> None:
        self._connection = sqlite3.connect(str(self._db_path))
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        self._connection.commit()

    def get_or_create_player(self, name: str) -> int:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
        self._connection.commit()
        return cursor.lastrowid

    def save_score(self, player_name: str, score: int) -> None:
        player_id = self.get_or_create_player(player_name)
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO scores (player_id, score) VALUES (?, ?)",
            (player_id, score),
        )
        self._connection.commit()

    def get_top_scores(self, limit: int = 10) -> list:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT p.name, s.score, s.created_at
            FROM scores s
            JOIN players p ON s.player_id = p.id
            ORDER BY s.score DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()

    def get_player_names(self) -> list[str]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT name FROM players ORDER BY name")
        return [row[0] for row in cursor.fetchall()]

    def close(self) -> None:
        if self._connection:
            self._connection.close()
