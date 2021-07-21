# 01. playRetroMario.py
# Play Super Mario Bros

import sys
import retro
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class RetroSuperMario(QWidget):
    # init
    def __init__(self):
        super().__init__()
        self.game_screen_resolution_multiples = 2
        self.key_state = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # [B, NULL, SELECT, START, U, D, L, R, A]
        # Set retro game
        self.emulator = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.emulator.reset()
        # Define screen info
        self.screen = self.emulator.get_screen()
        self.screen_width = self.screen.shape[0] * self.game_screen_resolution_multiples
        self.screen_height = self.screen.shape[1] * self.game_screen_resolution_multiples
        # Set window screen
        self.setFixedSize(self.screen_width, self.screen_height)
        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)
        # Set game timer (60 fps)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_screen)
        self.game_timer.start(1000 // 60)
        # Window show
        self.show()

    # Game screen update
    def update_screen(self):
        self.emulator.step(self.key_state)
        self.screen = self.emulator.get_screen()
        self.screen_qimage = QImage(self.screen, self.screen.shape[1], self.screen.shape[0], QImage.Format_RGB888)
        self.pixel_map = QPixmap(self.screen_qimage)
        self.pixel_map = self.pixel_map.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(self.pixel_map)

# Key press
    def keyPressEvent(self, event):
        key = event.key()
        # Move
        if key == 68:  # R
            self.key_state[7] = 1
        if key == 65:  # L
            self.key_state[6] = 1
        if key == 83:  # D
            self.key_state[5] = 1
        if key == 87:  # U
            self.key_state[4] = 1
        # Skill
        if key == 75:  # A
            self.key_state[8] = 1
        if key == 76:  # B
            self.key_state[0] = 1
        # Ui control
        if key == 44:  # SELECT
            self.key_state[2] = 1
        if key == 46:  # START
            self.key_state[3] = 1
        if key == 47:  # NULL
            self.key_state[1] = 1

    # Key release
    def keyReleaseEvent(self, event):
        key = event.key()
        # Move
        if key == 68:  # R
            self.key_state[7] = 0
        if key == 65:  # L
            self.key_state[6] = 0
        if key == 83:  # D
            self.key_state[5] = 0
        if key == 87:  # U
            self.key_state[4] = 0
        # Skill
        if key == 75:  # A
            self.key_state[8] = 0
        if key == 76:  # B
            self.key_state[0] = 0
        # Ui control
        if key == 44:  # SELECT
            self.key_state[2] = 0
        if key == 46:  # START
            self.key_state[3] = 0
        if key == 47:  # NULL
            self.key_state[1] = 0

# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RetroSuperMario()
    sys.exit(app.exec_())

