import sys
import math
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, QPoint, Qt


class Planet:
    def __init__(self, name, distance_from_sun, speed, density):
        self.name = name
        self.distance_from_sun = distance_from_sun
        self.rotation_speed = speed
        self.density = density
        self.angle = random.uniform(0, 360)  # Начальный угол вращения
        # Примерная масса планеты (по формуле шара)
        self.mass = density * (4 / 3) * math.pi * (self.distance_from_sun / 10) ** 3

    def increase_mass(self, amount):
        """Увеличивает массу планеты на заданное значение."""
        self.mass += amount

    def update_position(self):
        """Обновляет угол вращения и возвращает координаты планеты."""
        self.angle += self.rotation_speed  # Увеличиваем угол на скорость вращения
        x = self.distance_from_sun * math.cos(math.radians(self.angle))
        y = self.distance_from_sun * math.sin(math.radians(self.angle))
        return x, y


class Asteroid:
    def __init__(self, x, y, a_speed, a_direction, a_mass):
        self.x = x  # Координата X астероида
        self.y = y  # Координата Y астероида
        self.a_speed = a_speed
        self.a_direction = a_direction  # Угол направления в градусах
        self.a_mass = a_mass
        self.is_active = True  # Астероид активен по умолчанию

    def update_position(self):
        """Обновляет координаты астероида."""
        if self.is_active:
            self.x += self.a_speed * math.cos(math.radians(self.a_direction))
            self.y += self.a_speed * math.sin(math.radians(self.a_direction))
            # Проверяем выход за границы окна
            if self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 800:
                self.is_active = False  # Уничтожаем астероид


class SolarSystem(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализация параметров окна
        self.start_point = None
        self.setWindowTitle("Планетарная система")
        self.setGeometry(200, 0, 1000, 800)
        # Таймер для обновления состояния системы
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Обновляем каждые 50 мс

        # Создание планет с их характеристиками
        self.planets = [
            Planet("Меркурий", 58, 4.7, 5.42),
            Planet("Венера", 98, 3.50, 5.25),
            Planet("Земля", 140, 3.0, 5.515),
            Planet("Марс", 188, 2.4, 3.94),
            Planet("Юпитер", 248, 1.3, 1.33),
            Planet("Сатурн", 310, 0.97, 0.69),
            Planet("Уран", 375, 0.68, 1.29),
            Planet("Нептун", 457, 0.54, 1.64)
        ]
        # Цвета планет в формате RGB
        self.planets_color = [
            (169, 169, 169), (255, 215, 0), (30, 144, 255),
            (255, 99, 71), (255, 165, 0), (218, 165, 32),
            (135, 206, 250), (70, 130, 180)
        ]
        # Список астероидов
        self.asteroids = []

    def paintEvent(self, event):
        """Обрабатывает события рисования на экране."""
        painter = QPainter(self)
        # Рисуем фон
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(0, 0, self.width(), self.height())
        # Рисуем Солнце в центре окна
        painter.setPen(QColor(255, 255, 0))
        painter.setBrush(QColor(255, 255, 0))
        painter.drawEllipse(QPoint(self.width() // 2, self.height() // 2), 40, 40)
        for i in range(len(self.planets)):
            planet = self.planets[i]
            density_factor = int(255 * planet.density / max(p.density for p in self.planets))
            color = QColor(*self.planets_color[i], alpha=density_factor)
            painter.setBrush(color)
            painter.setPen(color)
            x_offset = planet.update_position()
            x = x_offset[0] + (self.width() // 2)
            y = x_offset[1] + (self.height() // 2)
            painter.drawEllipse(QPoint(int(x), int(y)), int(15 + i * 3), int(15 + i * 3))

        # Проверка столкновений с астероидами
        self.check_collisions()
        for asteroid in self.asteroids[:]:
            asteroid.update_position()
            if not asteroid.is_active:
                # Удаляем неактивные астероиды
                self.asteroids.remove(asteroid)
                continue

            painter.setPen(QColor(128, 128, 128))
            painter.setBrush(QColor(128, 128, 128))
            painter.drawEllipse(QPoint(int(asteroid.x), int(asteroid.y)), 5, 5)

    def mousePressEvent(self, event):
        """Обрабатывает нажатие кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Запоминаем начальную точку при нажатии кнопки мыши
            self.start_point = event.position()

    def mouseReleaseEvent(self, event):
        """Обрабатывает отпускание кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton and hasattr(self, 'start_point'):
            end_point = event.position()
            dx = end_point.x() - self.start_point.x()
            dy = end_point.y() - self.start_point.y()
            direction = math.degrees(math.atan2(dy, dx)) % 360
            speed = random.uniform(5.0, 15.0)
            mass = random.uniform(1.0, 10.0)
            asteroid = Asteroid(self.start_point.x(), self.start_point.y(), speed, direction, mass)
            self.asteroids.append(asteroid)

    def check_collisions(self):
        """Проверяет столкновения астероидов с Солнцем и планетами."""
        sun_x = self.width() // 2
        sun_y = self.height() // 2
        sun_radius = 40
        for asteroid in list(self.asteroids):
            if (asteroid.x - sun_x) ** 2 + (asteroid.y - sun_y) ** 2 <= sun_radius ** 2:
                self.asteroids.remove(asteroid)
                continue
            for planet in self.planets:
                planet_x_offset, planet_y_offset = planet.update_position()
                planet_x = planet_x_offset + (self.width() // 2)
                planet_y = planet_y_offset + (self.height() // 2)
                planet_radius = int(15 + planet.distance_from_sun / 10)
                if (asteroid.x - planet_x) ** 2 + (asteroid.y - planet_y) ** 2 <= planet_radius ** 2:
                    planet.density += 10
                    planet.increase_mass(1e10)
                    self.update_planet_color(planet)
                    self.asteroids.remove(asteroid)
                    break

    def update_planet_color(self, planet):
        """Обновляет цвет планеты в зависимости от её массы."""
        density_factor = int(255 * planet.density / max(p.density for p in self.planets))
        new_color = QColor(*self.planets_color[self.planets.index(planet)], alpha=density_factor)
        index = self.planets.index(planet)
        self.planets_color[index] = (new_color.red(), new_color.green(), new_color.blue())


# Запуск приложения
app = QApplication(sys.argv)
window = SolarSystem()
window.show()
app.exec()
