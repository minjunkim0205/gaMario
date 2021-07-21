# 01. labMarioChallenges1.py
import retro
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import numpy as np


class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        # 게임 해상도 배수
        self.gameScreenResolutionMultiples = 3
        # 게임 환경 생성
        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        # 새 게임 시작
        self.env.reset()
        # 화면 가져오기
        self.screen = self.env.get_screen()
        # 창 크기 고정
        print(self.screen.shape[0], self.screen.shape[1])
        self.setFixedSize(self.screen.shape[0]*self.gameScreenResolutionMultiples, self.screen.shape[1]*self.gameScreenResolutionMultiples)
        # 창 제목 설정
        self.setWindowTitle('GA Mario')

        # 이미지
        self.screen = self.env.get_screen()
        self.label_image = QLabel(self)
        self.image = np.array(self.screen)
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
        self.pixmap = QPixmap(self.qimage)
        self.pixmap = self.pixmap.scaled(self.screen.shape[0] * self.gameScreenResolutionMultiples, self.screen.shape[1] * self.gameScreenResolutionMultiples, Qt.IgnoreAspectRatio)
        self.label_image.setPixmap(self.pixmap)
        self.label_image.setGeometry(0, 0, self.screen.shape[0] * self.gameScreenResolutionMultiples, self.screen.shape[1] * self.gameScreenResolutionMultiples)
        self.show()



if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = GameScreen()
   sys.exit(app.exec_())