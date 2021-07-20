# 02. labMarioChallenges2.py
# 플레이 환경 만들기
import sys
import retro
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget

class Environment(QWidget):
    def __init__(self):
        super().__init__()
        # 게임 환경 생성
        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.env.reset()
        self.screen = self.env.get_screen()
        self.setFixedSize(self.screen.shape[0], self.screen.shape[1])
        self.setWindowTitle('GA Mario')
        # 1초에 60번 호출함수 정의
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.refresh)
        self.qtimer.start(1000 // 60)

    # 1초에 60번 호출
    def refresh(self):
        print("Test")

    # 키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()
        print(str(key) + ' press')

    # 키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        print(str(key) + ' release')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Environment()
    sys.exit(app.exec_())