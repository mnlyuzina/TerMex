import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from typing import Callable, overload

class Visualization3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.graph_objects = {
            'points': [],
            'vectors': [],
            'trails': []  # Список для шлейфов
        }

        # Настраиваем пределы осей
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])

        # Подписываем оси
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

    @overload
    def add_point(self, position: np.ndarray, color: str, label: str):
        ...

    @overload
    def add_point(self, update: Callable[[float], np.ndarray], color: str, label: str):
        ...

    def add_point(self, pos_or_update, color, label: str, trail_length=50):
        update = pos_or_update
        if isinstance(pos_or_update, np.ndarray):
            def update(_): return pos_or_update

        # Инициализация графического объекта для точки
        point_graph, = self.ax.plot([], [], [], color + 'o', label=label)
        self.graph_objects['points'].append((point_graph, update))

        # Инициализация шлейфа (линии)
        trail_graph, = self.ax.plot([], [], [], color=color, lw=1)  # Шлейф линии
        self.graph_objects['trails'].append((trail_graph, [], trail_length))  # Добавляем шлейф

    @overload
    def add_vector(self, update: Callable[[float], np.ndarray], color: str, label: str):
        ...

    @overload
    def add_vector(self, start: Callable[[float], np.ndarray], update: Callable[[float], np.ndarray], color: str, label: str):
        ...

    def add_vector(self, start: Callable[[float], np.ndarray], update: Callable[[float], np.ndarray], color: str, label: str = None):
        if label is None and isinstance(update, str):
            label = color
            color = update
            update = start
            def start(_): return np.zeros((3,))
        vector_graph = self.ax.quiver(0, 0, 0, 0, 0, 0, color=color, label=label)
        self.graph_objects['vectors'].append((vector_graph, start, color, label, update))

    def start_animation(self, start: float, end: float, number_of_frames: int, speed: float = 1.0):
        def update(frame):
            ret = []
            # Обновление точек
            for i, (point_graph, upd) in enumerate(self.graph_objects['points']):
                pos = upd(frame)
                point_graph.set_data([pos[0]], [pos[1]])  # Обновляем x и y
                point_graph.set_3d_properties([pos[2]])   # Обновляем z
                ret.append(point_graph)

                # Обновление шлейфа
                trail_graph, positions, trail_length = self.graph_objects['trails'][i]
                positions.append(pos)  # Сохраняем текущую позицию
                if len(positions) > trail_length:
                    positions.pop(0)  # Ограничиваем длину шлейфа

                # Обновляем данные шлейфа
                trail_positions = np.array(positions)
                trail_graph.set_data(trail_positions[:, 0], trail_positions[:, 1])
                trail_graph.set_3d_properties(trail_positions[:, 2])
                ret.append(trail_graph)

            # Обновление векторов
            for i, (vector_graph, start, color, label, upd) in enumerate(self.graph_objects['vectors']):
                vector_graph.remove()
                start_pos = start(frame)
                direction = upd(frame)
                vector_graph = self.ax.quiver(*start_pos, *direction, color=color, label=label)
                self.graph_objects['vectors'][i] = (vector_graph, start, color, label, upd)
                ret.append(vector_graph)

            return ret

        frames = np.linspace(start, end, number_of_frames)
        ani = FuncAnimation(self.fig, update, frames=frames, init_func=lambda: update(start), blit=False,
                            interval=1000 * (end - start) / (number_of_frames * speed))

        plt.legend()
        plt.show()
