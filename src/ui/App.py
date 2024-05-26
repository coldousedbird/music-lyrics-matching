# python src/ui/app.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel, QTextEdit, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from ui import Ui_MainWindow
from RequestHistoryDB import RequestHistoryDB
from datetime import datetime
import syncedlyrics



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("music_lyric_matcher")
        self.resize(600, 500)

        # COMMON LAYOUT
        app_layout = QVBoxLayout()
        self.setLayout(app_layout)

        # TABS INIT
        tabs = QTabWidget()
        tabs.setObjectName("tabs")
        app_layout.addWidget(tabs)
        
        # PROCESSING TAB SETUP
        self.processing = QWidget()
        self.processing.setObjectName("processing")
        tabs.addTab(self.processing, "processing")

        processing_layout = QVBoxLayout()
        self.processing.setLayout(processing_layout)

        # song loading
        self.song = None
        self.song_path = None
        load_song_btn = QPushButton("load song (.mp3/.wav)")
        processing_layout.addWidget(load_song_btn)
        load_song_btn.clicked.connect(self.on_click_load_song_btn)
        
        self.load_song_label = QLabel(" ")
        processing_layout.addWidget(self.load_song_label)
        
        # lyrics loading
        self.lyrics_path = None
        self.lyrics = None
        load_text_button = QPushButton("load lyrics (.txt)")
        processing_layout.addWidget(load_text_button)
        load_text_button.clicked.connect(self.on_click_load_lyrics_btn)

        self.load_lyrics_label = QLabel("")
        processing_layout.addWidget(self.load_lyrics_label)

        # processing btn
        self.result = None
        self.request_time = None
        processing_button = QPushButton("process")
        processing_layout.addWidget(processing_button)
        processing_button.clicked.connect(self.on_click_process_btn)

        self.processing_label = QLabel("result:")
        self.processing_result = QTextEdit("")
        processing_layout.addWidget(self.processing_label)
        processing_layout.addWidget(self.processing_result)

        # comment
        self.comment_label = QLabel("leave comment")
        self.comment_line = QLineEdit("")
        processing_layout.addWidget(self.comment_label)
        processing_layout.addWidget(self.comment_line)

        # save
        save_button = QPushButton("save")
        processing_layout.addWidget(save_button)
        self.save_label = QLabel("")
        processing_layout.addWidget(self.save_label)
        save_button.clicked.connect(self.on_click_save_btn)


        # DATA BASE SETUP
        DB_NAME = 'request_history.db'
        self.RequestHistoryDB = RequestHistoryDB()
        self.RequestHistoryDB.set_name(DB_NAME)

        # HISTORY TAB SETUP
        self.history = QWidget()
        self.history.setObjectName("history")
        tabs.addTab(self.history, "history")

        history_layout = QVBoxLayout()
        self.history.setLayout(history_layout)

        self.history_table = QTableWidget()
        history_layout.addWidget(self.history_table)

        self.update_history()

    def extract_filename(self, path):
        file = path.rsplit("/", 1)
        if len(path) > 1:
            return file[-1]
        else:
            return path

    def on_click_load_song_btn(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Audio files (*.mp3 *.wav)")
        if file_dialog.exec():
            self.song_path = file_dialog.selectedFiles()[0]
            with open(self.song_path, 'rb') as song:
                self.song = song.read()
            self.song_path = self.extract_filename(file_dialog.selectedFiles()[0])
            self.load_song_label.setText(f"selected: {self.song_path}")

    def on_click_load_lyrics_btn(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt)")
        if file_dialog.exec():
            self.lyrics_path = file_dialog.selectedFiles()[0]
            with open(self.lyrics_path, 'rb') as lyrics:
                self.lyrics = lyrics.read()
            self.lyrics_path = self.extract_filename(file_dialog.selectedFiles()[0])
            self.load_lyrics_label.setText(f"selected: {self.lyrics_path}")

    def process(self):
        # NOW IT'S LOADING SONGS LRCS FROM INTERNET USING SYNCEDLYRICS LIB
        try:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.result = syncedlyrics.search(self.song_path[0:-4])
            self.processing_result.setText(self.result)
        except Exception as e:
            self.processing_result.setText("\""+ str(e)+"\" error occured")
            return
        
        
        # LATER HERE MUST BE MODEL, WHICH WILL PROCESS FILES THROUGH



    def on_click_process_btn(self):
        if self.song and self.lyrics:
            self.processing_label.setText("result: ")
            self.process()
        elif not self.song:
            self.processing_label.setText("load song before processing")
        elif not self.lyrics:
            self.processing_label.setText("load lyrics before processing")

    def on_click_save_btn(self):
        if self.result:
            self.RequestHistoryDB.add(date=self.request_time, name=self.song_path, song=self.song, lyrics=self.lyrics, comment=self.comment_line.text())
            self.update_history()
            self.save_label.setText("success!")

    def update_history(self):
        requests = self.RequestHistoryDB.read()
        self.history_table.setRowCount(len(requests))
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["dates", "songs", "comments", "", ""])
        id = 0
        for request in requests:
            id += 1
            self.history_table.setItem(id, 0, QTableWidgetItem(request[0]))
            self.history_table.setItem(id, 1, QTableWidgetItem(request[1]))
            self.history_table.setItem(id, 2, QTableWidgetItem(request[4]))
            self.history_table.setItem(id, 3, QTableWidgetItem("listen"))
            self.history_table.setItem(id, 4, QTableWidgetItem("remove")) 




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())