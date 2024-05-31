import sqlite3

class RequestsDB:
    def __init__(self, name):
        self.name = name


    def create_new(self):
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

    def read(self):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT Date, Name, Comment FROM Requests").fetchall()
        
    def read_one(self, date):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT Name, Song, Lyrics FROM Requests WHERE Date = ?", (date,)).fetchall()[0]
            

    def add(self, date, name, song, lyrics, comment):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Requests (Date, Name, Song, Lyrics, Comment) VALUES (?, ?, ?, ?, ?) ON CONFLICT (DATE) DO NOTHING", 
                           (date, name, song, lyrics, comment))

    def remove(self, date):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Requests WHERE Date = ?", (date,))




if __name__ == "__main__":
    db = RequestsDB('request_history.db')
    db.create_new()