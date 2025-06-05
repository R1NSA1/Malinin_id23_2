import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer


class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  # начальный угол для точки на окружности
        self.radius = 200  # радиус окружности
        self.center = (300, 300)  # центр окна
        # таймер для обновления позиции точки
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)  # обновление каждые 50 мс

    def update_position(self):
        self.angle = (self.angle + 5) % 360  # увеличиваем угол на 5 градусов и обнуляем при достижении 360
        self.update()  # перерисовываем виджет

    def paintEvent(self, event):
        painter = QPainter(self)  # используем конструктор QPainter
        # рисуем окружность
        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse(self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2)
        # вычисляем координаты точки на окружности и преобразуем их в целые числа
        x = int(self.center[0] + self.radius * math.cos(math.radians(self.angle)))
        y = int(self.center[1] + self.radius * math.sin(math.radians(self.angle)))
        # рисуем точку
        painter.setBrush(QColor(255, 0, 0))  # цвет точки
        painter.drawEllipse(x - 10, y - 10, 20, 20)  # размер точки


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Малинин И. А. - 1 лаба")
        self.setFixedSize(600, 600)
        self.drawing_area = DrawingArea()
        self.setCentralWidget(self.drawing_area)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
