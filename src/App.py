# python src/ui/aзнерpp.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from RequestsDB import RequestsDB
from Processing import Processing
from ProcessingTab import ProcessingTab
from HistoryTab import HistoryTab

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("music_lyric_matcher")
        self.resize(600, 500)

        # DATA BASE SETUP
        DB_NAME = 'request_history.db'
        database = RequestsDB(DB_NAME)

        # COMMON LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # TABS INIT
        tabs = QTabWidget()
        tabs.setObjectName("tabs")
        layout.addWidget(tabs)
        
        # PROCESSING TAB SETUP
        self.processing_tab = ProcessingTab(database)
        self.processing_tab.setObjectName("processing")
        tabs.addTab(self.processing_tab, "processing")

        # HISTORY TAB SETUP
        self.history_tab = HistoryTab(database)
        self.history_tab.setObjectName("history")
        tabs.addTab(self.history_tab, "history")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())