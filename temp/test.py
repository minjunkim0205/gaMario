import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 고정
        self.setFixedSize(200, 300)
        # 창 제목 설정
        self.setWindowTitle('MyApp')
        # 창 띄우기
        self.show()

    # 창이 업데이트 될 때마다 실행되는 함수
    def paintEvent(self, event):
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        # RGB 색상으로 펜 설정
        painter.setPen(QPen(QColor.fromRgb(255, 0, 0), 3.0, Qt.SolidLine))
        # 브러쉬 설정 (채우기)
        painter.setBrush(QBrush(Qt.blue))
        # 직사각형 그리기
        painter.drawRect(0, 0, 100, 100)
        # 그리기 끝
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window2 = MyApp()
    sys.exit(app.exec_())