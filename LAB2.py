from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, QPoint
from PyQt6.QtWidgets import QMainWindow
import sys
import math
import random
import time

class Planets(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.initUI()
        self.start_time = time.time()
        self.initial_angles = [random.uniform(0, 360) for _ in range(8)]

    def initUI(self):
        self.setWindowTitle("Планеты (Малинин И. А.)")
        self.setGeometry(200, 0, 1000, 1000)
        self.setFixedSize(1000, 800)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0)) # sun and planets
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(0, 0, 1000, 1000)
        painter.setPen(QColor(255, 255, 0, 150))
        painter.setBrush(QColor(255, 255, 0, 150))
        painter.drawEllipse(QPoint(500, 400), 60, 60)
        elapsed_time = abs(time.time() - self.start_time) # planets coords
        r = 70
        planets_speed = [1.97, 1.85, 1.8, 1.74, 1.63, 1.597, 1.568, 1.554]
        planets_color = [(194, 202, 175), (255, 165, 0), (70, 130, 180), (195, 88, 23), (255, 197, 130), (255, 191, 85),
                         (0, 191, 255), (30, 144, 255)]

        def coordinates(c_x, c_y, r1, r2, speed=0, angele=0):
            angle_c = (elapsed_time * (speed_coefficient + speed) * 360 / (2 * math.pi)) + angele
            x = c_x + r1 * math.cos(math.radians(angle_c))
            y = c_y + r1 * math.sin(math.radians(angle_c))
            painter.drawEllipse(QPoint(int(x), int(y)), r2, r2)
            return int(x), int(y)

        for i, speed_coefficient in enumerate(planets_speed):
            painter.setPen(QColor(*planets_color[i], 150))
            painter.setBrush(QColor(*planets_color[i], 150))
            coord = coordinates(500, 400, r, 20, angele=self.initial_angles[i])
            if i >= 2:
                coordinates(coord[0], coord[1], 30, 3, speed=3)
                if i == 4:
                    coordinates(coord[0], coord[1], 30, 3, speed=2, angele=self.initial_angles[i])
                if i == 5:
                    painter.setBrush(QColor(*planets_color[i], 16))
                    painter.drawEllipse(QPoint(coord[0], coord[1]), 30, 30)
                    painter.drawEllipse(QPoint(coord[0], coord[1]), 35, 35)
            r += 20


app = QApplication(sys.argv)
window = Planets()
window.show()
app.exec()
