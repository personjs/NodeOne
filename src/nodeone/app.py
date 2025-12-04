import sys
from PyQt6.QtWidgets import QApplication
from nodeone.utils.logger import setup_logging
from nodeone.views.main_window import MainWindow

def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()