from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from nodeone.services.event_bus import EventBus


class DashboardWidget(QWidget):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard (Micro-frontend)"))

        self.ping_btn = QPushButton("Send ping to other plugins")
        layout.addWidget(self.ping_btn)

        self.last_msg = QLabel("No messages yet")
        layout.addWidget(self.last_msg)

        self.setLayout(layout)

    def _connect_signals(self):
        self.ping_btn.clicked.connect(self._send_ping)

    def _send_ping(self):
        self.event_bus.emit("ping", {"from": "dashboard"})

    def _on_event(self, name, payload):
        if name == "pong":
            self.last_msg.setText(f"Got pong: {payload}")


def create_plugin(event_bus):
    return DashboardWidget(event_bus)
