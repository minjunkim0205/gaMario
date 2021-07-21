# 04. pyqtChallenges5.py
# PyQt 1초마다 증가하는 타이머
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.time = 0
        # 창 크기 고정
        self.setFixedSize(200, 200)
        self.setWindowTitle('MyApp')
        self.keyLabel = QLabel(self)
        self.keyLabel.setGeometry(0, 0, 200, 200)
        self.show()
        # 타이머 설정
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timer)
        self.qtimer.start(1000)

    def timer(self):
        self.time = self.time + 1
        self.keyLabel.setText(str(self.time))

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   sys.exit(app.exec_())