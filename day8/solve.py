import math
from typing import NamedTuple
from heapq import heappush, heappop, nlargest


class Position(NamedTuple):
    x: int
    y: int
    z: int

    def distance(self, other: 'Position') -> int:
        result = (self.x - other.x) ** 2
        result += (self.y - other.y) ** 2
        result += (self.z - other.z) ** 2
        return result


class DSU:
    def __init__(self, n: int) -> None:
        self.size: list[int] = [1] * n
        self.refs: list[int] = list(range(n))

    def lookup(self, node: int) -> int:
        # parent node
        if self.refs[node] == node:
            return node

        self.refs[node] = self.lookup(self.refs[node])
        return self.refs[node]

    def connect(self, a: int, b: int) -> int:
        pa: int = self.lookup(a)
        pb: int = self.lookup(b)

        # the same set
        if pa == pb:
            return self.size[pa]

        # small optimization
        if self.size[pa] < self.size[pb]:
            pa, pb = pb, pa

        self.size[pa] += self.size[pb]
        self.size[pb] = 0
        self.refs[pb] = pa
        return self.size[pa]


def load(filename: str) -> list[Position]:
    with open(filename) as file:
        cords: list[Position] = []
        for line in file.readlines():
            x, y, z = map(int, line.strip().split(','))
            cords.append(Position(x=x, y=y, z=z))
        return cords


def build_pairs_priority_queue(cords: list[Position]) -> list[tuple[int, int, int]]:
    # queue item -> (distance, pair_idx, pair_jdx)
    priority_queue: list[tuple[int, int, int]] = []

    n: int = len(cords)
    for idx in range(n-1):
        for jdx in range(idx+1, n):
            distance: int = cords[idx].distance(cords[jdx])
            heappush(priority_queue, (distance, idx, jdx))

    return priority_queue


def part_one(cords: list[Position], limit: int) -> int:
    dsu = DSU(n=len(cords))
    pairs_pq: list[tuple[int, int, int]] = build_pairs_priority_queue(cords)

    while pairs_pq and limit:
        _, a, b = heappop(pairs_pq)
        dsu.connect(a, b)
        limit -= 1

    # get top 3 largest components sizes
    top_three_sizes: list[int] = nlargest(n=3, iterable=dsu.size)
    answer: int = math.prod(top_three_sizes)
    return answer


def part_two(cords: list[Position]) -> int:
    n: int = len(cords)
    dsu: DSU = DSU(n)
    pairs_pq: list[tuple[int, int, int]] = build_pairs_priority_queue(cords)

    while pairs_pq:
        _, a, b = heappop(pairs_pq)
        total: int = dsu.connect(a, b)

        # everything connected
        if total == n:
            return cords[a].x * cords[b].x

    return -1


if __name__ == '__main__':
    limit: int = 10
    filename: str = 'example.txt'

    cords: list[Position] = load(filename)

    part_one_: int = part_one(cords, limit=limit)
    part_two_: int = part_two(cords)

    print(f'Part I: {part_one_}')
    print(f'Part II: {part_two_}')

