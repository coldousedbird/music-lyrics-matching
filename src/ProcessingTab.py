from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox
from Processing import Processing
from RequestsDB import RequestsDB

# for test_ProcessingTab
from sys import argv, exit
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog

class ProcessingTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # DATA BASE SETUP
        DB_NAME = 'request_history.db'
        self.database = RequestsDB(DB_NAME)

        self.processing = Processing()

        # BASIC GROUPBOXES AND LAYOUTS
        layout = QVBoxLayout()
        self.setLayout(layout)

        load_box = QGroupBox(self)
        layout.addWidget(load_box)
        load_layout = QVBoxLayout()
        load_box.setLayout(load_layout)

        self.process_box = QGroupBox(self)
        self.process_box.hide()
        layout.addWidget(self.process_box)
        process_layout = QVBoxLayout()
        self.process_box.setLayout(process_layout)

        self.result_box = QGroupBox(self)
        self.result_box.hide()
        layout.addWidget(self.result_box)
        result_layout = QVBoxLayout()
        self.result_box.setLayout(result_layout)

        # WIDGETS
        # LOADING
        load_song_btn = QPushButton("load song (.mp3/.wav)")
        load_layout.addWidget(load_song_btn)
        load_song_btn.clicked.connect(self.on_click_load_song_btn)
        
        self.load_song_label = QLabel("")
        load_layout.addWidget(self.load_song_label)

        # load_text_button = QPushButton("load lyrics (.txt)")
        # load_layout.addWidget(load_text_button)
        # load_text_button.clicked.connect(self.on_click_load_lyrics_btn)

        # self.load_lyrics_label = QLabel("")
        # load_layout.addWidget(self.load_lyrics_label)
        
        # PROCESSING
        find_button = QPushButton("try find .lrc in internet")
        process_layout.addWidget(find_button)
        find_button.clicked.connect(self.on_click_find_btn)

        recognize_button = QPushButton("recognize lyrics")
        process_layout.addWidget(recognize_button)
        recognize_button.clicked.connect(self.on_click_recognize_btn)

        # RESULT
        self.result_label = QLabel("result:")
        result_layout.addWidget(self.result_label)
        self.result_text = QTextEdit("")
        result_layout.addWidget(self.result_text)

        self.comment_label = QLabel("comment")
        self.comment_line = QLineEdit("")
        result_layout.addWidget(self.comment_label)
        result_layout.addWidget(self.comment_line)

        # save
        comment_button = QPushButton("add comment")
        result_layout.addWidget(comment_button)
        comment_button.clicked.connect(self.on_click_comment_btn)

    def throw_messagebox(self, title_text: str, text: str, icon: QMessageBox.Icon) -> None:
        message_box = QMessageBox()
        message_box.setWindowTitle(title_text)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def on_click_load_song_btn(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Audio files (*.mp3 *.wav)")
        if file_dialog.exec():
            path = file_dialog.selectedFiles()[0]
            self.processing.load_song(path)
            self.load_song_label.setText(f"selected: {self.processing.song_name}")
            self.result_text.setText("")
            self.process_box.show()
            self.result_box.hide()

    # def on_click_load_lyrics_btn(self) -> None:
    #     file_dialog = QFileDialog(self)
    #     file_dialog.setNameFilter("Text files (*.txt)")
    #     if file_dialog.exec():
    #         path = file_dialog.selectedFiles()[0]
    #         self.processing.load_lyrics(path)
    #         self.load_lyrics_label.setText(f"selected: {self.processing.lyrics_name}")

    def on_click_find_btn(self) -> None:
        self.result_text.setText("")
        if self.processing.song: # and self.processing.lyrics
            self.processing.find_lrc()
            if self.processing.result: 
                self.database.add_request(date=self.processing.request_time, 
                    name=self.processing.song_name, 
                    song=self.processing.song, 
                    lyrics=self.processing.result)
                self.result_text.setText(self.processing.result)
                self.result_box.show()
            else:
                self.result_text.setText("not found")

        elif not self.processing.song:
            self.throw_messagebox("Warning", "Load song before starting the processing.", QMessageBox.Icon.Warning)
        # elif not self.processing.lyrics:
        #     self.throw_messagebox("Warning", "Load lyrics before start of the processing.", QMessageBox.Icon.Warning)

    def on_click_recognize_btn(self) -> None:
        self.result_text.setText("")
        if self.processing.song: # and self.processing.lyrics
            self.processing.make_lrc()
            self.database.add_request(date=self.processing.request_time, 
                    name=self.processing.song_name, 
                    song=self.processing.song, 
                    lyrics=self.processing.result)
            self.result_text.setText(self.processing.result)
            self.result_box.show()
                
        elif not self.processing.song:
            self.throw_messagebox("Warning", "Load song before start of the processing.", QMessageBox.Icon.Warning)

    def on_click_comment_btn(self) -> None:
        if self.processing.result and self.comment_line.Text:
            self.database.add_comment(self.processing.request_time, self.comment_line.text())
            self.throw_messagebox("Information", "Comment saved successfully.", QMessageBox.Icon.Information)
        else:
            self.throw_messagebox("Warning", "You have nothing to save yet.", QMessageBox.Icon.Warning)


def test_ProcessingTab() -> None:
    app = QApplication(argv)
    window = ProcessingTab()
    window.show()
    exit(app.exec())

if __name__ == "__main__":
    test_ProcessingTab()