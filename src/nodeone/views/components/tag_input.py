from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QPushButton, 
    QHBoxLayout, QVBoxLayout, QFrame, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from nodeone.utils.logger import get_logger

logger = get_logger(__name__)

class TagWidget(QFrame):
    removed = pyqtSignal(str)
    
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Label for the tag text
        self.label = QLabel(text)
        
        # Button to remove the tag
        self.remove_button = QPushButton("X")
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        
        layout.addWidget(self.label)
        layout.addWidget(self.remove_button)
        
        self.setLayout(layout)
        self.setStyleSheet("TagWidget { background-color: #e0e0e0; border-radius: 5px; }")
        
    def _on_remove_clicked(self):
        # Emit the signal so the parent widget can handle removal
        self.removed.emit(self.text)
        self.deleteLater() # Safely delete the widget
        
        
class TagInputWidget(QWidget):
    """A custom component combining a line edit and a list of tags."""
    
    # Signal emitted when a new tag is successfully added
    tag_added = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter a tag and press Enter")
        # Connect the 'Enter' key press to our handler
        self.lineEdit.returnPressed.connect(self.add_tag_from_input)
        
        main_layout.addWidget(self.lineEdit)
        
        # 2. Container for the dynamically created tags
        # We use a QVBoxLayout to stack tags vertically
        self.tags_container = QWidget()
        self.tags_layout = QVBoxLayout()
        self.tags_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align tags to the top
        self.tags_layout.setContentsMargins(0, 0, 0, 0)
        self.tags_container.setLayout(self.tags_layout)
        
        main_layout.addWidget(self.tags_container)
        
        # Add a stretch to push everything to the top visually
        main_layout.addStretch() 

        self.setLayout(main_layout)
        self.current_tags = set() # Keep track of existing tags
        
    def _connect_signals(self):
        pass

    def add_tag_from_input(self):
        """Processes text from QLineEdit when Enter is pressed."""
        text = self.lineEdit.text().strip()
        if text and text not in self.current_tags:
            self.add_tag(text)
            self.lineEdit.clear()
        elif text in self.current_tags:
            # Optional: provide user feedback that tag exists
            self.lineEdit.setStyleSheet("QLineEdit { border: 1px solid red; }")
        
    def add_tag(self, text: str):
        """Creates and adds a new TagWidget."""
        tag_widget = TagWidget(text)
        # Connect the tag's remove signal to our handler
        tag_widget.removed.connect(self.remove_tag)
        
        self.tags_layout.addWidget(tag_widget)
        self.current_tags.add(text)
        self.tag_added.emit(text)

    def remove_tag(self, text: str):
        """Removes a TagWidget and updates the internal list."""
        self.current_tags.remove(text)
        # The TagWidget handles its own deletion via deleteLater()
        logger.debug(f"Removed tag: {text}")

    def get_all_tags(self) -> list:
        """Returns a list of all current tags."""
        return list(self.current_tags)