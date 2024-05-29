# python src/ui/app.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel, QTextEdit, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from RequestsDB import RequestsDB
from Processing import Processing
from ProcessingTab import ProcessingTab
from HistoryTab import HistoryTab

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("music_lyric_matcher")
        self.resize(600, 500)

        # # PROCESSING MODULE SETUP
        # self.Processing = Processing()

        # DATA BASE SETUP
        DB_NAME = 'request_history.db'
        self.database = RequestsDB()
        self.database.set_name(DB_NAME)

        # COMMON LAYOUT
        app_layout = QVBoxLayout()
        self.setLayout(app_layout)

        # TABS INIT
        tabs = QTabWidget()
        tabs.setObjectName("tabs")
        app_layout.addWidget(tabs)
        
        # PROCESSING TAB SETUP
        self.processing_tab = ProcessingTab(self.database)
        self.processing_tab.setObjectName("processing")
        tabs.addTab(self.processing_tab, "processing")

        # HISTORY TAB SETUP
        self.history_tab = HistoryTab(self.database)
        self.history_tab.setObjectName("history")
        tabs.addTab(self.history_tab, "history")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())