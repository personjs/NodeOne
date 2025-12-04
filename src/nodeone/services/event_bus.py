from PyQt6.QtCore import QObject, pyqtSignal


class EventBus(QObject):
    """
    A simple event bus based on Qt signals.
    Plugins and the shell can connect to these signals to communicate.
    """

    event_signal = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()

    def emit(self, name: str, payload: object = None):
        # convenience wrapper
        self.event_signal.emit(name, payload)
