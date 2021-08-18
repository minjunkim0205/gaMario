# 09. labMarioChallenges9.py
# 회면정보를 date 에 넣어서 ai 모델처리후 랜덤 플레이 하게 만들어보기

import sys
import retro
import numpy as np
import tensorflow as tf
#np.set_printoptions(threshold=sys.maxsize)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
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
        self.setWindowTitle("Game")
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
        self.emulator_ram = self.emulator.get_ram()

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
        self.aiKeyPressEvent()

    def aiKeyPressEvent(self):
        try:
            self.aiKeyInput = analysis_window.result
        except:
            self.aiKeyInput = [0, 0, 0, 0, 0, 0]
        # 이동
        if self.aiKeyInput[0] == 1:  # R
            self.key_state[7] = 1
        if self.aiKeyInput[1] == 1:  # L
            self.key_state[6] = 1
        if self.aiKeyInput[2] == 1:  # D
            self.key_state[5] = 1
        if self.aiKeyInput[3] == 1:  # U
            self.key_state[4] = 1

        if self.aiKeyInput[0] == 0:  # R
            self.key_state[7] = 0
        if self.aiKeyInput[1] == 0:  # L
            self.key_state[6] = 0
        if self.aiKeyInput[2] == 0:  # D
            self.key_state[5] = 0
        if self.aiKeyInput[3] == 0:  # U
            self.key_state[4] = 0
        # 대쉬(스킬), 점프
        if self.aiKeyInput[4] == 1:  # A
            self.key_state[0] = 1
        if self.aiKeyInput[5] == 1:  # B
            self.key_state[8] = 1

        if self.aiKeyInput[4] == 0:  # A
            self.key_state[0] = 0
        if self.aiKeyInput[5] == 0:  # B
            self.key_state[8] = 0
    '''
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
    '''
class VisualAnalysis(QWidget):
    # init
    def __init__(self):
        super().__init__()
        # 원도우 창 정보 정의
        self.analysis_screen_width = 16 * 16
        self.analysis_screen_height = 16 * 13
        # 원도우 창 설정
        self.setWindowTitle("Visual Analysis")
        self.setFixedSize(self.analysis_screen_width, self.analysis_screen_height)
        self.analysis_screen_label = QLabel(self)
        self.analysis_screen_label.setGeometry(0, 0, self.analysis_screen_width, self.analysis_screen_height)
        # 게임 타이머 설정 (60헤르츠)
        self.analysis_timer = QTimer(self)
        self.analysis_timer.timeout.connect(self.refresh)
        self.analysis_timer.start(1000 // 60)
        # 원도우 띄우기
        self.show()
        # Ai모델 설정
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(9, input_shape=(13 * 16,), activation='relu'),
            tf.keras.layers.Dense(6, activation='sigmoid')
        ])

    def refresh(self):
        self.update()

    # 창이 업데이트 될 때마다 실행되는 함수
    def paintEvent(self, event):
        # 화면 정보를 케싱
        self.full_screen_tiles_raw = game_window.emulator_ram[0x0500:0x069F + 1]
        self.full_screen_tile_count = self.full_screen_tiles_raw.shape[0]
        self.full_screen_page1_tile = self.full_screen_tiles_raw[:self.full_screen_tile_count // 2].reshape((13, 16))
        self.full_screen_page2_tile = self.full_screen_tiles_raw[self.full_screen_tile_count // 2:].reshape((13, 16))
        self.full_screen_tiles = np.concatenate((self.full_screen_page1_tile, self.full_screen_page2_tile), axis=1).astype(np.int)
        # 플레이어 {(0,0)시작}좌표를 full_screen_tiles 에 덮어 씌우기
        self.full_screen_tiles_player_x = (((game_window.emulator_ram[0x0086]+1)+((game_window.emulator_ram[0x006D]%2)*255))//16)%32
        self.full_screen_tiles_player_y = ((game_window.emulator_ram[0x00CE]-1)//16)%13
        self.full_screen_tiles[self.full_screen_tiles_player_y][self.full_screen_tiles_player_x]=-1
        # 적 {(0,0)시작}좌표를 full_screen_tiles 에 덮어 씌우기
        for i in range(5):
            if(game_window.emulator_ram[0x000F+i] == 1):
                self.full_screen_tiles_enemies_x = (((game_window.emulator_ram[0x0087+i]+1)+((game_window.emulator_ram[0x006E+i]%2)*255))//16)%32
                self.full_screen_tiles_enemies_y = ((game_window.emulator_ram[0x00CF+i]-9)//16)%13
                self.full_screen_tiles[self.full_screen_tiles_enemies_y][self.full_screen_tiles_enemies_x] = -2
        # 전체 화면을 슬라이싱해 화면 잘라내기
        self.screen_start_position = (((game_window.emulator_ram[0x071C]+1)+((game_window.emulator_ram[0x071A]%2)*255))//16)%32
        self.transformed_screen_tiles_raw = np.concatenate((self.full_screen_tiles, self.full_screen_tiles), axis=1).astype(np.int)
        self.transformed_screen_tiles = self.transformed_screen_tiles_raw[0:13, self.screen_start_position:self.screen_start_position+16]
        # 플레이어의 진행 거리 출력
        #print((game_window.emulator_ram[0x0086]+1)+(game_window.emulator_ram[0x006D]*255))
        # 뉴럴 네트워크 모델
        self.date = self.transformed_screen_tiles.flatten()
        self.predict = self.model.predict(np.array([self.date]))[0]
        self.result = (self.predict > 0.5).astype(np.int)
        print(self.result)

        '''
        # Empty = 0x00 - 0
        # Fake = 0x01 - 1
        # Ground = 0x54 - 84
        # Top_Pipe1 = 0x12 - 18
        # Top_Pipe2 = 0x13 - 19
        # Bottom_Pipe1 = 0x14 - 20
        # Bottom_Pipe2 = 0x15 - 21
        # Flagpole_Top =  0x24 - 36
        # Flagpole = 0x25 - 37
        # Coin_Block1 = 0xC0 - 192
        # Coin_Block2 = 0xC1 - 193
        # Coin = 0xC2 - 194
        # Breakable_Block = 0x51 - 81
        '''
        # 그래픽 설정
        self.graphic = QPainter()
        self.graphic.begin(self)
        self.graphic.setPen(QPen(QColor.fromRgb(0, 0, 0), 0.1, Qt.SolidLine))
        # 픽셀화 맵 그리기
        for i in range(13):
            for j in range(16):
                # 플레이어는 푸른색으로 출력
                if self.transformed_screen_tiles[i][j] == -1:
                    self.graphic.setBrush(QBrush(QColor.fromRgb(0, 191, 255)))
                # 적은 빨간색으로 출력
                elif self.transformed_screen_tiles[i][j] == -2:
                    self.graphic.setBrush(QBrush(QColor.fromRgb(230, 25, 25)))
                # 빈공간 혹은 코인은 흰색으로 출력
                elif self.transformed_screen_tiles[i][j] == 0 or self.transformed_screen_tiles[i][j] == 194:
                    self.graphic.setBrush(QBrush(QColor.fromRgb(255, 255, 255)))
                # 도착 깃발은 초록색으로 출력
                elif self.transformed_screen_tiles[i][j] == 36 or self.transformed_screen_tiles[i][j] == 37:
                    self.graphic.setBrush(QBrush(QColor.fromRgb(178, 230, 25)))
                # 밟을수 있는 나머지 블럭은 모두 갈색
                else:
                    self.graphic.setBrush(QBrush(QColor.fromRgb(150, 75, 0)))
                self.graphic.drawRect(16*j, 16*i, 16, 16)
        self.graphic.end()

# 메인
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_window = RetroSuperMario()
    analysis_window = VisualAnalysis()
    sys.exit(app.exec_())
