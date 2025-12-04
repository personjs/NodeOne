from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtGui import QColor, QPainter, QFont
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, Qt, pyqtProperty # type: ignore

class NavButton(QPushButton):
    """Theme-aware navbar button with automatic hover color."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._hover_progress = 0.0
        self.setMouseTracking(True)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Smooth hover animation
        self.hover_anim = QPropertyAnimation(self, b"hover_progress", parent)
        self.hover_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setStyleSheet("border: none; padding: 6px 14px;")

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_anim.stop()
        self.hover_anim.setDuration(200)
        self.hover_anim.setStartValue(self._hover_progress)
        self.hover_anim.setEndValue(1.0)
        self.hover_anim.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.hover_anim.stop()
        self.hover_anim.setDuration(200)
        self.hover_anim.setStartValue(self._hover_progress)
        self.hover_anim.setEndValue(0.0)
        self.hover_anim.start()

    def paintEvent(self, a0):
        super().paintEvent(a0)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Theme foreground
        fg = self.palette().color(self.palette().ColorRole.WindowText)

        # Hover/press overlay
        bg = fg
        bg.setAlpha(int(30 * self._hover_progress))

        painter.fillRect(self.rect(), bg)
        painter.setPen(fg)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()
        
    @pyqtProperty(float)
    def hover_progress(self) -> float: # type: ignore
        return self._hover_progress
        
    @hover_progress.setter # type: ignore
    def hover_progress(self, value: float):
        self._hover_progress = value
        self.update()


class Navbar(QWidget):
    """A modern translucent navbar with theme-aware colors."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(56)

        # Entire row layout
        main = QHBoxLayout(self)
        main.setContentsMargins(20, 0, 20, 0)
        main.setSpacing(20)

        # Sections
        self.left = QHBoxLayout()
        self.center = QHBoxLayout()
        self.right = QHBoxLayout()

        # Stretch ensures center stays centered
        main.addLayout(self.left)
        main.addStretch(1)
        main.addLayout(self.center)
        main.addStretch(1)
        main.addLayout(self.right)

        # Theme-aware background
        self._updatePaletteColors()

    def _updatePaletteColors(self):
        palette = self.palette()
        self.bg = palette.color(palette.ColorRole.Window)
        self.fg = palette.color(palette.ColorRole.WindowText)

        # Apply theme-aware text color to child widgets
        self.setStyleSheet(
            f"background-color: {self.bg.name()}; color: {self.fg.name()};"
        )

    def addLeft(self, widget: QWidget):
        self.left.addWidget(widget)

    def addCenter(self, widget: QWidget):
        self.center.addWidget(widget)

    def addRight(self, widget: QWidget):
        self.right.addWidget(widget)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        painter = QPainter(self)

        # ===========================
        #   Modern Glass Background
        # ===========================
        glass = QColor(self.bg)
        glass.setAlpha(200)  # semi-transparent for modern effect
        painter.fillRect(self.rect(), glass)

        # ===========================
        #   Bottom Divider Line
        # ===========================
        shadow = QColor(self.fg)
        shadow.setAlpha(60)
        painter.fillRect(QRect(0, self.height() - 1, self.width(), 1), shadow)
