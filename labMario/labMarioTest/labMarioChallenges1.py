# 01. labMarioChallenges1.py
import retro
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,\
    QWidget, QLabel, QPushButton
import numpy as np


class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        # 게임 해상도 배수
        gameScreenResolutionMultiples = 3
        # 게임 환경 생성
        env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        # 새 게임 시작
        env.reset()
        # 화면 가져오기
        screen = env.get_screen()
        # 창 크기 고정
        print(screen.shape[0], screen.shape[1])
        self.setFixedSize(screen.shape[0]*gameScreenResolutionMultiples, screen.shape[1]*gameScreenResolutionMultiples)
        # 창 제목 설정
        self.setWindowTitle('GA Mario')

        # 이미지
        label_image = QLabel(self)

        image = np.array(screen)
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(screen.shape[0]*gameScreenResolutionMultiples, screen.shape[1]*gameScreenResolutionMultiples, Qt.IgnoreAspectRatio)

        print(screen)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0, 0, screen.shape[0]*gameScreenResolutionMultiples, screen.shape[1]*gameScreenResolutionMultiples)

        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = GameScreen()
   sys.exit(app.exec_())