# python src/ui/aзнерpp.py
from sys import argv, exit
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget


from ProcessingTab import ProcessingTab
from HistoryTab import HistoryTab

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("music_lyric_matcher")
        self.resize(700, 800)

        # COMMON LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # TABS INIT
        tabs = QTabWidget()
        tabs.setObjectName("tabs")
        layout.addWidget(tabs)
        
        # PROCESSING TAB SETUP
        self.processing_tab = ProcessingTab()
        self.processing_tab.setObjectName("processing")
        tabs.addTab(self.processing_tab, "processing")

        # HISTORY TAB SETUP
        self.history_tab = HistoryTab()
        self.history_tab.setObjectName("history")
        tabs.addTab(self.history_tab, "history")

def main() -> None:
    app = QApplication(argv)
    window = App()
    window.show()
    exit(app.exec())

if __name__ == "__main__":
    main()