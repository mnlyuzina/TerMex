import numpy as np
import sympy as sp

# Определение переменной времени
t = sp.symbols('t')

class MaterialPoint:
    def __init__(self, position_law):
        self.__position_law = position_law
        self.__velocity_law = [sp.diff(component, t, 1) for component in position_law]
        self.__acceleration_law = [sp.diff(component, t, 2) for component in position_law]

    # Метод для получения координат точки в заданный момент времени
    def get_position(self, time: float) -> np.ndarray:
        return np.array([float(comp.subs(t, time).evalf()) for comp in self.__position_law])

    # Метод для получения скорости точки в заданный момент времени
    def get_velocity(self, time: float) -> np.ndarray:
        return np.array([float(comp.subs(t, time).evalf()) for comp in self.__velocity_law])

    # Метод для получения ускорения точки в заданный момент времени
    def get_acceleration(self, time: float) -> np.ndarray:
        return np.array([float(comp.subs(t, time).evalf()) for comp in self.__acceleration_law])

    # Метод для получения тангенциального вектора в заданный момент времени
    def get_tangential(self, time: float) -> np.ndarray:
        velocity = self.get_velocity(time)
        return velocity / np.linalg.norm(velocity)

    # Метод для получения нормального вектора в заданный момент времени
    def get_normal(self, time: float) -> np.ndarray:
        acceleration = self.get_acceleration(time)
        return acceleration / np.linalg.norm(acceleration)

    # Метод для получения бинормального вектора в заданный момент времени
    def get_binormal(self, time: float) -> np.ndarray:
        tangential = self.get_tangential(time)
        normal = self.get_normal(time)
        return np.cross(tangential, normal)

# Пример использования класса MaterialPoint
if __name__ == '__main__':
    example_position_law = [
        sp.cos(t) * sp.sin(2 * t),
        sp.sin(t) * sp.cos(2 * t),
        sp.sin(3 * t)
    ]

    material_point = MaterialPoint(example_position_law)
    position_at_time_1 = material_point.get_position(1)
    print(type(position_at_time_1))
    for coord in position_at_time_1:
        print(type(coord))
