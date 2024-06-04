import sqlite3
from os import _exists

class RequestsDB:
    def __init__(self, name: str) -> None:
        self.name = name

        DATABASE_DOESNT_EXIST = not _exists(self.name)

        if DATABASE_DOESNT_EXIST: # then create new 
            with sqlite3.connect(self.name) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Requests (
                        Date TEXT PRIMARY KEY NOT NULL, 
                        Name TEXT NOT NULL,
                        Song BLOB NOT NULL, 
                        Lyrics TEXT NOT NULL, 
                        Comment TEXT)
                ''')

    def get_all_requests(self: str) -> list[str, str, str]:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT Date, Name, Comment FROM Requests").fetchall()
        
    def get_request_data(self, date: str) -> list[str, bytes, str]:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT Name, Song, Lyrics FROM Requests WHERE Date = ?", (date,)).fetchall()[0]
    
    def add_request(self, date: str, name: str, song: bytes, lyrics: str) -> None:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Requests (Date, Name, Song, Lyrics) VALUES (?, ?, ?, ?) ON CONFLICT (DATE) DO NOTHING", 
                           (date, name, song, lyrics))
            
    def add_comment(self, date: str, comment: str):
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Requests SET Comment = ? WHERE Date = ?", 
                           (comment, date))

    def remove_request(self, date: str) -> None:
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Requests WHERE Date = ?", (date,))


def test_database() -> None:
    db = RequestsDB('request_history.db')

if __name__ == "__main__":
    test_database()