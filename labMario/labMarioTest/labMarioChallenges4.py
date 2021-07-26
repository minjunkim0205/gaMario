# 02. labMarioChallenges4.py
# 램값 분석해서 케릭터 정보를 출력해 보기

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
        self.key_state = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # [B, NULL, SELECT, START, U, D, L, R, A]
        # 레트로 모듈 설정
        self.emulator = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.emulator.reset()
        # 게임 화면 정보 정의
        self.game_screen_resolution_multiples = 2
        self.game_screen = self.emulator.get_screen()
        self.game_screen_width = self.game_screen.shape[0] * self.game_screen_resolution_multiples
        self.game_screen_height = self.game_screen.shape[1] * self.game_screen_resolution_multiples
        # 원도우 창 설정
        self.setFixedSize(self.game_screen_width, self.game_screen_height)
        self.game_screen_label = QLabel(self)
        self.game_screen_label.setGeometry(0, 0, self.game_screen_width, self.game_screen_height)
        # 게임 타이머 설정 (60헤르츠)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.refresh)
        self.game_timer.start(1000 // 60)
        # 원도우 띄우기
        self.show()

    # 게임 키 상태 업데이트
    def updateGameKeyState(self):
        self.emulator.step(self.key_state)

    # 게임 램값 케싱 업데이트
    def updateGameRamInfo(self):
        self.emulator_map_tiles = self.emulator.get_screen()
        # print(self.emulator_map_tiles[223][239])  # 16x16 | 224 x 240
        self.emulator_ram = self.emulator.get_ram()
        # print("Size:" + str(self.emulator_ram.shape[0]))
        print("Player's state | HEX:0x000E | value:" + str(self.emulator_ram[int("0x000E", 16)]))
        print("Info:Player screen x | HEX:0x03AD | value:" + str(self.emulator_ram[int("0x03AD", 16)]))
        print("Info:Player screen y | HEX:0x00CE | value:" + str(self.emulator_ram[int("0x00CE", 16)]))

    # 게임 화면 업데이트
    def updateGameScreen(self):
        self.game_screen = self.emulator.get_screen()
        self.game_screen_qimage = QImage(self.game_screen, self.game_screen.shape[1], self.game_screen.shape[0], QImage.Format_RGB888)
        self.pixel_map = QPixmap(self.game_screen_qimage)
        self.pixel_map = self.pixel_map.scaled(self.game_screen_width, self.game_screen_height, Qt.IgnoreAspectRatio)
        self.game_screen_label.setPixmap(self.pixel_map)

    # 60 프레임으로 리프레시
    def refresh(self):
        self.updateGameKeyState()
        self.updateGameScreen()
        self.updateGameRamInfo()

    # 키 누르기
    def keyPressEvent(self, event):
        self.key = event.key()
        # 이동
        if self.key == 68:  # R
            self.key_state[7] = 1
        if self.key == 65:  # L
            self.key_state[6] = 1
        if self.key == 83:  # D
            self.key_state[5] = 1
        if self.key == 87:  # U
            self.key_state[4] = 1
        # 스킬
        if self.key == 75:  # A
            self.key_state[0] = 1
        if self.key == 76:  # B
            self.key_state[8] = 1
        # 선택화면 컨트롤 키
        if self.key == 44:  # SELECT
            self.key_state[2] = 1
        if self.key == 46:  # START
            self.key_state[3] = 1
        if self.key == 47:  # NULL
            self.key_state[1] = 1
        # 디버깅용 키
        if self.key == 82:
            self.emulator.reset()

    # 키 때기
    def keyReleaseEvent(self, event):
        self.key = event.key()
        # 이동
        if self.key == 68:  # R
            self.key_state[7] = 0
        if self.key == 65:  # L
            self.key_state[6] = 0
        if self.key == 83:  # D
            self.key_state[5] = 0
        if self.key == 87:  # U
            self.key_state[4] = 0
        # 스킬
        if self.key == 75:  # A
            self.key_state[0] = 0
        if self.key == 76:  # B
            self.key_state[8] = 0
        # 선택화면 컨트롤 키
        if self.key == 44:  # SELECT
            self.key_state[2] = 0
        if self.key == 46:  # START
            self.key_state[3] = 0
        if self.key == 47:  # NULL
            self.key_state[1] = 0

# 메인
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RetroSuperMario()
    sys.exit(app.exec_())

