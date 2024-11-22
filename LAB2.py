import sys
import math
import random
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, QPoint


class Planet:
    def __init__(self, name, distance_from_sun, speed, density):
        self.name = name
        self.distance_from_sun = distance_from_sun
        self.speed = speed
        self.density = density
        self.angle = random.uniform(0, 360)

    def update_position(self):
        # обновляем угол и возвращаем координаты планеты
        self.angle += self.speed  # увеличиваем угол на фиксированное значение скорости
        x = self.distance_from_sun * math.cos(math.radians(self.angle))
        y = self.distance_from_sun * math.sin(math.radians(self.angle))
        return x, y


class SolarSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планетарная система")
        self.setGeometry(200, 0, 1000, 800)
        self.setFixedSize(1000, 800)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(18)  # Обновляем каждые 50 мс

        self.planets = [Planet("Меркурий", 58, 4.7, 5.42),
                        Planet("Венера", 98, 3.50, 5.25),
                        Planet("Земля", 140, 3.0, 5.515),
                        Planet("Марс", 188, 2.4, 3.94),
                        Planet("Юпитер", 248, 1.3, 1.33),
                        Planet("Сатурн", 310, 0.97, 0.69),
                        Planet("Уран", 375, 0.68, 1.29),
                        Planet("Нептун", 457, 0.54, 1.64)]

        self.planets_color = [(169, 169, 169),
                              (255, 215, 0),
                              (30, 144, 255),
                              (255, 99, 71),
                              (255, 165, 0),
                              (218, 165, 32),
                              (135, 206, 250),
                              (70, 130, 180)]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0)) # рисуем фон
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setPen(QColor(255, 255, 0)) # рисуем солнце
        painter.setBrush(QColor(255, 255, 0))
        painter.drawEllipse(QPoint(self.width() // 2, self.height() // 2), 40, 40)
        for i in range(len(self.planets)):
            planet = self.planets[i]
            color = QColor(*self.planets_color[i])
            painter.setPen(color)
            painter.setBrush(color)
            # устанавливаем цвет планеты в зависимости от ее плотности
            density_factor = int(255 * planet.density / max(p.density for p in self.planets))
            color = QColor(*self.planets_color[self.planets.index(planet)], alpha=density_factor)
            painter.setPen(color)
            painter.setBrush(color)
            x_offset = planet.update_position() # получаем координаты планеты
            x = x_offset[0] + (self.width() // 2)
            y = x_offset[1] + (self.height() // 2)
            painter.drawEllipse(QPoint(int(x), int(y)), int(15 + i * 3), int(15 + i * 3))   # рисуем планету


app = QApplication(sys.argv)
window = SolarSystem()
window.show()
sys.exit(app.exec())