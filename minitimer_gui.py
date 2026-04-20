#!/usr/bin/env python3
#
# FILE: minitimer_gui.py
# AUTHOR: Miguel Salvá
# ABSTRACT: PySide6 GUI for the Pomodoro-based minitimer
#
# Run with: python minitimer_gui.py

import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QPushButton,
)
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    Property, QPointF, QRectF,
)
from PySide6.QtGui import (
    QPainter, QPainterPath, QColor, QLinearGradient,
    QRadialGradient, QFont, QPen, QBrush, QIcon,
)

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALARM_PATH = os.path.join(SCRIPT_DIR, "vinyl-piano_100bpm_C_minor.mp3")
LOGO_PATH  = os.path.join(SCRIPT_DIR, "images", "minitimer_logo.png")

DEFAULT_SECONDS = 1500  # 25 minutes

PRESETS = [
    ("5m",  300),
    ("15m", 900),
    ("25m", 1500),
    ("45m", 2700),
]

# ── Palette ────────────────────────────────────────────────────────────────────
C_RED_BRIGHT    = QColor("#FF6B6B")
C_RED_MID       = QColor("#E63946")
C_RED_DEEP      = QColor("#C1121F")
C_GREEN_SOFT    = QColor("#52B788")
C_AMBER         = QColor("#FFD166")
C_BG_DARK       = QColor("#0F0F23")
C_BG_MID        = QColor("#16213E")
C_BG_PANEL      = QColor(22, 33, 62, 230)
C_WHITE         = QColor("#FAFAFA")
C_MUTED         = QColor("#8B8FA8")
C_RING_TRACK    = QColor(255, 255, 255, 20)
C_BTN_GHOST     = QColor(255, 255, 255, 14)
C_BTN_HOVER     = QColor(255, 255, 255, 28)
C_BORDER        = QColor(255, 255, 255, 22)


# ── Helpers ────────────────────────────────────────────────────────────────────
def play_alarm():
    from PySide6.QtCore import QProcess
    QProcess().startDetached("afplay", [ALARM_PATH])


def progress_color(p: float) -> QColor:
    """Return a color that transitions green → amber → red as p goes 1→0."""
    if p > 0.5:
        return C_GREEN_SOFT
    if p > 0.25:
        return C_AMBER
    return C_RED_MID


# ── Circular progress ring ─────────────────────────────────────────────────────
class RingWidget(QWidget):
    """
    A clean circular progress ring with the countdown in the centre.
    No decorations — purely typographic + geometric.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(220, 220)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._remaining = DEFAULT_SECONDS
        self._total     = DEFAULT_SECONDS
        self._running   = False

        # Subtle scale pulse while running
        self._pulse = 1.0
        self._anim = QPropertyAnimation(self, b"pulse")
        self._anim.setDuration(1100)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(1.025)
        self._anim.setEasingCurve(QEasingCurve.InOutSine)
        self._anim.setLoopCount(-1)

    # Qt property ──────────────────────────────────────────────────────────────
    def _get_pulse(self):       return self._pulse
    def _set_pulse(self, v):    self._pulse = v; self.update()
    pulse = Property(float, _get_pulse, _set_pulse)

    # Public API ───────────────────────────────────────────────────────────────
    def set_state(self, remaining: int, total: int, running: bool):
        was_running = self._running
        self._remaining = remaining
        self._total     = total
        self._running   = running

        if running and not was_running:
            self._anim.start()
        elif not running and was_running:
            self._anim.stop()
            self._pulse = 1.0

        self.update()

    # Paint ────────────────────────────────────────────────────────────────────
    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        side  = min(w, h)
        cx, cy = w / 2, h / 2

        # Apply pulse scale from centre
        painter.translate(cx, cy)
        painter.scale(self._pulse, self._pulse)
        painter.translate(-cx, -cy)

        margin   = 20
        ring_w   = 10          # track stroke width
        prog_w   = 10          # progress stroke width
        r        = (side - 2 * margin) / 2
        arc_rect = QRectF(cx - r, cy - r, r * 2, r * 2)

        # ── Track ring ─────────────────────────────────────────────────────
        painter.setPen(QPen(C_RING_TRACK, ring_w, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(arc_rect)

        # ── Progress arc ───────────────────────────────────────────────────
        progress = self._remaining / self._total if self._total else 0.0
        col = progress_color(progress)
        pen = QPen(col, prog_w, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        start = 90 * 16
        span  = int(progress * 360 * 16)
        painter.drawArc(arc_rect, start, span)

        # ── Inner glow dot at arc tip ──────────────────────────────────────
        if progress > 0.005:
            import math
            angle_rad = math.radians(90 - progress * 360)
            tip_x = cx + r * math.cos(angle_rad)
            tip_y = cy - r * math.sin(angle_rad)
            dot_r = prog_w / 2 + 1
            glow_grad = QRadialGradient(QPointF(tip_x, tip_y), dot_r * 3)
            glow_col = QColor(col)
            glow_col.setAlpha(80)
            glow_grad.setColorAt(0, glow_col)
            glow_grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(glow_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(tip_x, tip_y), dot_r * 3, dot_r * 3)

            painter.setBrush(QBrush(col))
            painter.drawEllipse(QPointF(tip_x, tip_y), dot_r, dot_r)

        # ── Countdown text ─────────────────────────────────────────────────
        minutes = self._remaining // 60
        secs    = self._remaining % 60
        time_str = f"{minutes:02d}:{secs:02d}"

        font = QFont(".AppleSystemUIFont", int(side * 0.21), QFont.Light)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        painter.setFont(font)
        painter.setPen(C_WHITE)
        painter.drawText(QRectF(0, 0, w, h), Qt.AlignCenter, time_str)


# ── Glass panel background ─────────────────────────────────────────────────────
class PanelWidget(QWidget):
    """Rounded glass card with subtle border."""
    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, 20, 20)
        painter.setBrush(QBrush(C_BG_PANEL))
        painter.setPen(QPen(C_BORDER, 1))
        painter.drawPath(path)


# ── Full-window gradient background ───────────────────────────────────────────
class BackgroundWidget(QWidget):
    def paintEvent(self, _):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0.0, QColor("#0F0F23"))
        grad.setColorAt(1.0, QColor("#16213E"))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, w, h)


# ── Pill button ────────────────────────────────────────────────────────────────
class PillButton(QPushButton):
    """Rounded pill button: ghost or solid-accent variant."""

    def __init__(self, text: str, accent: bool = False, parent=None):
        super().__init__(text, parent)
        self._accent  = accent
        self._hovered = False
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setFont(QFont(".AppleSystemUIFont", 13, QFont.Medium))

    def enterEvent(self, e): self._hovered = True;  self.update(); super().enterEvent(e)
    def leaveEvent(self, e): self._hovered = False; self.update(); super().leaveEvent(e)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, h / 2, h / 2)

        if self._accent:
            base = C_RED_MID if not self._hovered else C_RED_BRIGHT
            painter.setBrush(QBrush(base))
            painter.setPen(Qt.NoPen)
        else:
            bg = C_BTN_HOVER if self._hovered else C_BTN_GHOST
            painter.setBrush(QBrush(bg))
            painter.setPen(QPen(C_BORDER, 1))

        painter.drawPath(path)
        painter.setPen(C_WHITE)
        painter.setFont(self.font())
        painter.drawText(0, 0, w, h, Qt.AlignCenter, self.text())


# ── Small preset chip ─────────────────────────────────────────────────────────
class ChipButton(QPushButton):
    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self._selected = False
        self._hovered  = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)
        self.setFont(QFont(".AppleSystemUIFont", 12))

    def set_selected(self, v: bool): self._selected = v; self.update()
    def enterEvent(self, e): self._hovered = True;  self.update(); super().enterEvent(e)
    def leaveEvent(self, e): self._hovered = False; self.update(); super().leaveEvent(e)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, h / 2, h / 2)

        if self._selected:
            painter.setBrush(QBrush(C_RED_MID))
            painter.setPen(Qt.NoPen)
            text_color = C_WHITE
        elif self._hovered:
            painter.setBrush(QBrush(C_BTN_HOVER))
            painter.setPen(QPen(C_BORDER, 1))
            text_color = C_WHITE
        else:
            painter.setBrush(QBrush(C_BTN_GHOST))
            painter.setPen(QPen(C_BORDER, 1))
            text_color = C_MUTED

        painter.drawPath(path)
        painter.setPen(text_color)
        painter.setFont(self.font())
        painter.drawText(0, 0, w, h, Qt.AlignCenter, self.text())


# ── Separator line ────────────────────────────────────────────────────────────
class Separator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setPen(QPen(C_BORDER, 1))
        painter.drawLine(0, 0, self.width(), 0)


# ── Main window ────────────────────────────────────────────────────────────────
class MinitimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("minitimer")
        self.setMinimumSize(360, 520)
        self.resize(400, 560)
        if os.path.exists(LOGO_PATH):
            self.setWindowIcon(QIcon(LOGO_PATH))

        self._total     = DEFAULT_SECONDS
        self._remaining = DEFAULT_SECONDS
        self._running   = False

        self._qt_timer = QTimer(self)
        self._qt_timer.setInterval(1000)
        self._qt_timer.timeout.connect(self._tick)

        self._build_ui()

    # ── Build ──────────────────────────────────────────────────────────────────
    def _build_ui(self):
        bg = BackgroundWidget()
        self.setCentralWidget(bg)

        # Outer layout with padding
        outer = QVBoxLayout(bg)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(0)

        # ── Card panel ──────────────────────────────────────────────────────
        panel = PanelWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 28, 24, 28)
        panel_layout.setSpacing(0)
        outer.addWidget(panel)

        # Title
        title = QLabel("minitimer")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont(".AppleSystemUIFont", 17, QFont.Medium)
        title.setFont(title_font)
        title.setStyleSheet("color: #FAFAFA; letter-spacing: 1px;")
        panel_layout.addWidget(title)

        panel_layout.addSpacing(4)

        # Session label
        self._session_lbl = QLabel("Focus Session")
        self._session_lbl.setAlignment(Qt.AlignCenter)
        self._session_lbl.setFont(QFont(".AppleSystemUIFont", 11))
        self._session_lbl.setStyleSheet("color: #8B8FA8;")
        panel_layout.addWidget(self._session_lbl)

        panel_layout.addSpacing(28)

        # Ring
        self._ring = RingWidget()
        self._ring.set_state(self._remaining, self._total, False)
        panel_layout.addWidget(self._ring, stretch=1)

        panel_layout.addSpacing(28)

        # Separator
        panel_layout.addWidget(Separator())
        panel_layout.addSpacing(20)

        # Presets
        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        self._chips: list[ChipButton] = []
        for i, (label, secs) in enumerate(PRESETS):
            chip = ChipButton(label)
            chip.clicked.connect(lambda _, s=secs, idx=i: self._select_preset(s, idx))
            chip.set_selected(secs == DEFAULT_SECONDS)
            self._chips.append(chip)
            preset_row.addWidget(chip)
        panel_layout.addLayout(preset_row)

        panel_layout.addSpacing(16)

        # Control buttons
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        self._btn_play = PillButton("Start", accent=True)
        self._btn_play.clicked.connect(self._on_play)
        ctrl_row.addWidget(self._btn_play, stretch=2)

        self._btn_reset = PillButton("Reset")
        self._btn_reset.clicked.connect(self._on_reset)
        ctrl_row.addWidget(self._btn_reset, stretch=1)

        panel_layout.addLayout(ctrl_row)

    # ── Timer logic ────────────────────────────────────────────────────────────
    def _tick(self):
        if self._remaining > 0:
            self._remaining -= 1
            self._ring.set_state(self._remaining, self._total, self._running)
        else:
            self._qt_timer.stop()
            self._running = False
            self._ring.set_state(0, self._total, False)
            self._btn_play.setText("Start")
            self._session_lbl.setText("Session complete ✓")
            play_alarm()

    def _on_play(self):
        if self._running:
            self._qt_timer.stop()
            self._running = False
            self._btn_play.setText("Resume")
        else:
            if self._remaining == 0:
                self._remaining = self._total
            self._qt_timer.start()
            self._running = True
            self._btn_play.setText("Pause")
        self._ring.set_state(self._remaining, self._total, self._running)

    def _on_reset(self):
        self._qt_timer.stop()
        self._running   = False
        self._remaining = self._total
        self._btn_play.setText("Start")
        self._session_lbl.setText("Focus Session")
        self._ring.set_state(self._remaining, self._total, False)

    def _select_preset(self, seconds: int, idx: int):
        self._qt_timer.stop()
        self._running   = False
        self._total     = seconds
        self._remaining = seconds
        self._btn_play.setText("Start")
        self._session_lbl.setText("Focus Session")
        self._ring.set_state(self._remaining, self._total, False)
        for i, chip in enumerate(self._chips):
            chip.set_selected(i == idx)


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("minitimer")
    app.setOrganizationName("miguelsalva")
    app.setFont(QFont(".AppleSystemUIFont", 13))

    win = MinitimerWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
