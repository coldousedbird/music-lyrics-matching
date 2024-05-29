from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from functools import partial


class HistoryTab(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database

        layout = QVBoxLayout()
        self.setLayout(layout)

        update_history_btn = QPushButton("update history")
        update_history_btn.clicked.connect(self.update_history)
        layout.addWidget(update_history_btn)


        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.update_history()

    def listen_request(self, date):
        song, lyrics = self.database.read_one(date)
        # with open("temp/playing_song.mp3", "wb") as audio:
        #     audio = song
        print("listen btn pressed: ", date)
        
    def remove_request(self, date):
        self.database.remove(date)
        self.update_history()


    def update_history(self):
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["date", "song", "comment", "", ""])
        requests = self.database.read()
        self.table.setRowCount(len(requests))

        id = 0
        for request in requests:
            self.table.setItem(id, 0, QTableWidgetItem(request[0]))
            self.table.setItem(id, 1, QTableWidgetItem(request[1]))
            self.table.setItem(id, 2, QTableWidgetItem(request[4]))

            listen_btn = QPushButton("listen")
            listen_btn.clicked.connect(partial(self.listen_request, request[0]))
            self.table.setCellWidget(id, 3, listen_btn)
            
            remove_btn = QPushButton("remove")
            remove_btn.clicked.connect(partial(self.remove_request, request[0]))
            self.table.setCellWidget(id, 4, remove_btn) 

            id += 1