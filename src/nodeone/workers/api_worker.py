from PyQt6.QtCore import QThread, pyqtSignal
import requests

API_URL = "https://jsonplaceholder.typicode.com/todos/1"

class ApiWorker(QThread):
    """
    A background worker thread that fetches from an API.
    """
    result_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def run(self):
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            self.result_signal.emit(response.json())
        except Exception as e:
            self.error_signal.emit(str(e))