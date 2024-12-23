from visual import Visualization3D
from point import MaterialPoint, t
import sympy as sp

# Определение закона движения точки
position_law = [
    sp.cos(t),
    sp.sin(t),
    sp.cos(2 * t)
]

# Инициализация объектов
visualizer = Visualization3D()
material_point = MaterialPoint(position_law)

# Временные интервалы
start_time = 0
end_time = 50

# Добавление движущейся точки
visualizer.add_point(lambda time: material_point.get_position(time), 'k', 'Материальная точка', trail_length=1000)

# Добавление радиус-вектора
visualizer.add_vector(lambda time: material_point.get_position(time), 'r', 'Радиус-вектор')

# Добавление вектора скорости
visualizer.add_vector(lambda time: material_point.get_position(time), lambda time: material_point.get_velocity(time), 'y', 'Вектор скорости')

# Добавление вектора ускорения
visualizer.add_vector(lambda time: material_point.get_position(time), lambda time: material_point.get_acceleration(time), 'm', 'Вектор ускорения')

# Добавление тангенциального, нормального и бинормального векторов
visualizer.add_vector(lambda time: material_point.get_position(time), lambda time: material_point.get_tangential(time), 'b', label='Тангенциальный вектор')
visualizer.add_vector(lambda time: material_point.get_position(time), lambda time: material_point.get_normal(time), 'g', label='Нормальный вектор')
visualizer.add_vector(lambda time: material_point.get_position(time), lambda time: material_point.get_binormal(time), 'c', label='Бинормальный вектор')

# Запуск анимации
visualizer.start_animation(start_time, end_time, 5000, speed=0.5)
