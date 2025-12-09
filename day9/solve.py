import math
from typing import NamedTuple
from heapq import heappush, heappop, nlargest

import matplotlib.pyplot as plt
from shapely.geometry import Polygon


class Position(NamedTuple):
    x: int
    y: int

    def square(self, other: 'Position'):
        width: int = abs(self.x - other.x) + 1
        height: int = abs(self.y - other.y) + 1
        return width * height


def load(filename: str) -> list[Position]:
    with open(filename) as file:
        cords: list[Position] = []
        for line in file.readlines():
            x, y = map(int, line.strip().split(','))
            cords.append(Position(x=x, y=y))
        return cords


def show(cords: list[Position]) -> None:
    polygon: Polygon = Polygon(cords)

    x, y = polygon.exterior.xy

    plt.figure(figsize=(8,12))
    plt.plot(x, y, linewidth=1)
    plt.fill(x, y, alpha=0.3)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def build_rectangle(a: Position, b: Position) -> Polygon:
    x1, y1 = a
    x2, y2 = b
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    return Polygon([(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)])


def solve(cords: list[Position]) -> tuple[int, int]:
    part_one: int = 0
    part_two: int = 0
    n: int = len(cords)

    polygon: Polygon = Polygon(cords)

    for i in range(n-1):
        for j in range(i+1, n):
            a: Position = cords[i]
            b: Position = cords[j]

            square: int = a.square(b)
            part_one = max(part_one, square)

            rectangle: Polygon = build_rectangle(a, b)
            if polygon.contains(rectangle):
                part_two = max(part_two, square)

    return part_one, part_two


if __name__ == '__main__':
    filename: str = 'example.txt'
    cords: list[Position] = load(filename)

    part_one, part_two = solve(cords)

    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')

