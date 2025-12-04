from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from nodeone.services.event_bus import EventBus
from nodeone.services.theme_manager import ThemeManager
from nodeone.views.components.navbar import NavButton, Navbar
from nodeone.utils.logger import get_logger
from nodeone.models.settings import settings
from nodeone.workers.api_worker import ApiWorker

logger = get_logger(__name__)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_bus = EventBus()
        self.theme_manager = ThemeManager()

        self._setup_ui()
        self._connect_signals()
        
        self.theme_manager.apply_theme(self)

    def _setup_ui(self):
        self.setWindowTitle(settings.ui.name)
        self.resize(settings.ui.width, settings.ui.height)

        layout = QVBoxLayout(self)

        # Navigation
        self.nav = Navbar(self)
        self.nav.addLeft(NavButton("App"))
        self.nav.addCenter(NavButton("Home"))
        self.nav.addCenter(NavButton("About"))
        self.nav.addRight(NavButton("Settings"))
        layout.addWidget(self.nav)

        # Main content filler
        content = QLabel("Main Content Area")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)
        
        self.button = QPushButton("Call API")
        self.label = QLabel("Press button to call API")
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        
    def _connect_signals(self):
        self.button.clicked.connect(self.call_api)
        
    def call_api(self):
        self.label.setText("Calling API...")
        
        self.worker = ApiWorker()
        self.worker.result_signal.connect(self.handle_response)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.start()
        
    def handle_response(self, data: dict):
        self.label.setText(f"Received: {data.get('title')}")
        logger.info(f"data: {data}")
        
    def handle_error(self, err: str):
        self.label.setText(f"Error: {err}")