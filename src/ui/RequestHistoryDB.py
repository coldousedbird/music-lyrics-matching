import sqlite3

class RequestHistoryDB:
    def set_name(self, name):
        self.name = name


    def create_new(self, name):
        self.set_name(name)
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Requests (
                    Date TEXT PRIMARY KEY, 
                    Name TEXT,
                    Song BLOB NOT NULL, 
                    Lyrics BLOB NOT NULL, 
                    Comment TEXT)
            ''')

    def read(self):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT * FROM Requests").fetchall()
        
    def read_one(self, date):
        if not self.name:
            return
        with sqlite3.connect(self.name) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT * FROM Requests WHERE Date = ?", (date,)).fetchall()

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
    db = RequestHistoryDB()
    db.create_new(name = 'request_history.db')