# 02. labMarioChallenges2.py
# 마리오 게임 플레이 하기

import sys
import retro
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class RetroSuperMario(QWidget):
    def __init__(self):
        super().__init__()
        self.game_screen_resolution_multiples = 2
        self.key_state = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # [B, NULL, SELECT, START, U, D, L, R, A]
        # 레트로 게임 설정
        self.emulator = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.emulator.reset()
        # 화면 정보 정의
        self.screen = self.emulator.get_screen()
        self.screen_width = self.screen.shape[0] * self.game_screen_resolution_multiples
        self.screen_height = self.screen.shape[1] * self.game_screen_resolution_multiples
        # 창 사이즈 설정
        self.setFixedSize(self.screen_width, self.screen_height)
        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)
        # 게임 타이머 설정
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_screen)
        self.game_timer.start(1000 // 30)
        # 창 띄우기
        self.show()

    # 게임 화면 리프레시
    def update_screen(self):
        self.emulator.step(self.key_state)
        self.screen = self.emulator.get_screen()
        self.screen_qimage = QImage(self.screen, self.screen.shape[1], self.screen.shape[0], QImage.Format_RGB888)
        self.pixel_map = QPixmap(self.screen_qimage)
        self.pixel_map = self.pixel_map.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(self.pixel_map)

    # 키를 눌렀을때
    def keyPressEvent(self, event):
        key = event.key()
        # 움직이기
        if key == 68:  # R
            self.key_state[7] = 1
        if key == 65:  # L
            self.key_state[6] = 1
        if key == 83:  # D
            self.key_state[5] = 1
        if key == 87:  # U
            self.key_state[4] = 1
        # 스킬
        if key == 75:  # A
            self.key_state[8] = 1
        if key == 76:  # B
            self.key_state[0] = 1

    # 키를 땠을때
    def keyReleaseEvent(self, event):
        key = event.key()
        # 움직이기
        if key == 68:  # R
            self.key_state[7] = 0
        if key == 65:  # L
            self.key_state[6] = 0
        if key == 83:  # D
            self.key_state[5] = 0
        if key == 87:  # U
            self.key_state[4] = 0
        # 스킬
        if key == 75:  # A
            self.key_state[8] = 0
        if key == 76:  # B
            self.key_state[0] = 0

# 메인
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RetroSuperMario()
    sys.exit(app.exec_())

