from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox
from Processing import Processing


class ProcessingTab(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.processing = Processing()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # song loading
        load_song_btn = QPushButton("load song (.mp3/.wav)")
        layout.addWidget(load_song_btn)
        load_song_btn.clicked.connect(self.on_click_load_song_btn)
        
        self.load_song_label = QLabel("")
        layout.addWidget(self.load_song_label)
        
        # lyrics loading
        load_text_button = QPushButton("load lyrics (.txt)")
        layout.addWidget(load_text_button)
        load_text_button.clicked.connect(self.on_click_load_lyrics_btn)

        self.load_lyrics_label = QLabel("")
        layout.addWidget(self.load_lyrics_label)

        # processing btn
        process_button = QPushButton("process")
        layout.addWidget(process_button)
        process_button.clicked.connect(self.on_click_process_btn)

        self.result_label = QLabel("result:")
        layout.addWidget(self.result_label)
        self.result_text = QTextEdit("")
        layout.addWidget(self.result_text)

        # comment
        self.comment_label = QLabel("leave comment")
        self.comment_line = QLineEdit("")
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_line)

        # save
        save_button = QPushButton("save")
        layout.addWidget(save_button)
        save_button.clicked.connect(self.on_click_save_btn)

    def extract_filename(self, path):
        file = path.rsplit("/", 1)
        return file[-1] if len(path) > 1 else path

    def throw_messagebox(self, title_text, text, icon):
        message_box = QMessageBox()
        message_box.setWindowTitle(title_text)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        message_box.exec()


    def on_click_load_song_btn(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Audio files (*.mp3 *.wav)")
        if file_dialog.exec():
            self.processing.song_path = file_dialog.selectedFiles()[0]
            with open(self.processing.song_path, 'rb') as song:
                self.processing.song = song.read()
            self.processing.song_path = self.extract_filename(file_dialog.selectedFiles()[0])
            self.load_song_label.setText(f"selected: {self.processing.song_path}")

    def on_click_load_lyrics_btn(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt)")
        if file_dialog.exec():
            self.processing.lyrics_path = file_dialog.selectedFiles()[0]
            with open(self.processing.lyrics_path, 'r') as lyrics:
                self.processing.lyrics = lyrics.read()
            self.processing.lyrics_path = self.extract_filename(file_dialog.selectedFiles()[0])
            self.load_lyrics_label.setText(f"selected: {self.processing.lyrics_path}")

    def on_click_process_btn(self):
        if self.processing.song and self.processing.lyrics:
            self.processing.process()
            if self.processing.result:
                self.result_text.setText(self.processing.result)
            else:
                self.result_text.setText("not found")
        elif not self.processing.song:
            self.throw_messagebox("Warning", "Load song before start of the processing.", QMessageBox.Icon.Warning)
        elif not self.processing.lyrics:
            self.throw_messagebox("Warning", "Load lyrics before start of the processing.", QMessageBox.Icon.Warning)


    def on_click_save_btn(self):
        if self.processing.result:
            self.database.add(date=self.processing.request_time, 
                                      name=self.processing.song_path, 
                                      song=self.processing.song, 
                                      lyrics=self.processing.result, 
                                      comment=self.comment_line.text())
            self.throw_messagebox("Information", "Request saved successfully.", QMessageBox.Icon.Information)
        else:
            self.throw_messagebox("Warning", "You have nothing to save yet.", QMessageBox.Icon.Warning)