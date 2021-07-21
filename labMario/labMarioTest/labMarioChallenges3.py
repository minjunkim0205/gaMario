# 03. labMarioChallenges3.py
# 슈퍼마리오 게임 램값 케싱해서 표시하기

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
        # 레트로 모듈 설정
        self.emulator = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.emulator.reset()
        # 레트로 게임 램값 케싱
        self.emulator_ram = self.emulator.get_ram()
        # 원도우 창 정보 정의
        self.screen = self.emulator.get_screen()
        self.screen_width = self.screen.shape[0] * self.game_screen_resolution_multiples
        self.screen_height = self.screen.shape[1] * self.game_screen_resolution_multiples
        # 원도우 창 설정
        self.setFixedSize(self.screen_width, self.screen_height)
        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)
        # 게임 타이머 설정 (60헤르츠)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.refresh)
        self.game_timer.start(1000 // 60)
        # 원도우 띄우기
        self.show()

    # 게임 키 상태 업데이트
    def updateGameKeyState(self):
        self.emulator.step(self.key_state)

    # 게임 화면 업데이트
    def updateGameScreen(self):
        self.screen = self.emulator.get_screen()
        self.screen_qimage = QImage(self.screen, self.screen.shape[1], self.screen.shape[0], QImage.Format_RGB888)
        self.pixel_map = QPixmap(self.screen_qimage)
        self.pixel_map = self.pixel_map.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(self.pixel_map)

    # 게임 램값 케싱 업데이트
    def updateGameRamInfo(self):
        self.emulator_ram = self.emulator.get_ram()
        print("Size:" + str(self.emulator_ram.shape))
        print("Info:Lives | HEX:0x075A | value:" + str(self.emulator_ram[int("0x075A", 16)]))
        print("Info:Coins | HEX:0x075E | value:" + str(self.emulator_ram[int("0x075E", 16)]))

    # 60 프레임으로 리프레시
    def refresh(self):
        self.updateGameKeyState()
        self.updateGameScreen()
        self.updateGameRamInfo()

    # 키 누르기
    def keyPressEvent(self, event):
        key = event.key()
        # 이동
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
        # 선택화면 컨트롤 키
        if key == 44:  # SELECT
            self.key_state[2] = 1
        if key == 46:  # START
            self.key_state[3] = 1
        if key == 47:  # NULL
            self.key_state[1] = 1

    # 키 때기
    def keyReleaseEvent(self, event):
        key = event.key()
        # 이동
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
        # 선택화면 컨트롤 키
        if key == 44:  # SELECT
            self.key_state[2] = 0
        if key == 46:  # START
            self.key_state[3] = 0
        if key == 47:  # NULL
            self.key_state[1] = 0

# 메인
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RetroSuperMario()
    sys.exit(app.exec_())

