from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from functools import partial
from os import getenv
from RequestsDB import RequestsDB


class HistoryTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        # DATA BASE SETUP
        DB_NAME = 'request_history.db'
        self.database = RequestsDB(DB_NAME)

        layout = QVBoxLayout()
        self.setLayout(layout)

        update_history_btn = QPushButton("update history")
        update_history_btn.clicked.connect(self.update_history)
        layout.addWidget(update_history_btn)


        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.update_history()

    def download_request(self, date: str) -> None:
        dir_path = QFileDialog.getExistingDirectory(
            caption="Select directory to download",
            directory=getenv("HOME"),
        )
        name, song, lyrics = self.database.get_request(date)

        path = dir_path + "/" + name
        with open(path, "wb") as file:
            file.write(song)
        path = path[:-4] + ".lrc"
        with open(path, "w") as file:
            file.write(lyrics)

    def remove_request(self, date: str) -> None:
        message_box = QMessageBox()
        message_box.setWindowTitle("Warning")
        message_box.setText("Are you sure? This action is not reversible.")
        message_box.setIcon(QMessageBox.Icon.Warning)
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message_box.setDefaultButton(QMessageBox.StandardButton.No)
        reply = message_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.database.remove_request(date)
            self.update_history()

    def update_history(self) -> None:
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["date", "song", "comment", "", ""])
        requests = self.database.get_all_requests()
        self.table.setRowCount(len(requests))

        id = 0
        for request in requests:
            self.table.setItem(id, 0, QTableWidgetItem(request[0]))
            self.table.setItem(id, 1, QTableWidgetItem(request[1]))
            self.table.setItem(id, 2, QTableWidgetItem(request[2]))

            download_btn = QPushButton("download")
            download_btn.clicked.connect(partial(self.download_request, request[0]))
            self.table.setCellWidget(id, 3, download_btn)
            
            remove_btn = QPushButton("remove")
            remove_btn.clicked.connect(partial(self.remove_request, request[0]))
            self.table.setCellWidget(id, 4, remove_btn) 

            id += 1