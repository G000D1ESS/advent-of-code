import re
from dataclasses import dataclass


BLOCK_SIZE: int = 9
SIZE_COEF: float = 7 / 9


@dataclass
class Puzzle:
    n: int
    m: int
    to_use: list[int]


def load(filename: str) -> list[Puzzle]:
    with open(filename) as file:
        data: list[Puzzle] = []

        for line in file.readlines():
            if match := re.match(r'^(\d+)x(\d+): (.+)$', line.strip()):
                n, m, to_use = match.groups()

                n: int = int(n)
                m: int = int(m)
                to_use: list[int] = list(map(int, to_use.strip().split(' ')))

                puzzle = Puzzle(n=n, m=m, to_use=to_use)
                data.append(puzzle)

        return data


def solve(data: list[Puzzle]) -> int:
    total: int = 0

    for puzzle in data:
        empty_space: int = puzzle.n * puzzle.m
        regions: int = sum(puzzle.to_use)

        required: int = int(regions * BLOCK_SIZE * SIZE_COEF)
        if required <= empty_space:
            total += 1

    return total


if __name__ == '__main__':
    filename: str = 'example.txt'
    filename: str = 'puzzle.txt'

    data: list[Puzzle] = load(filename)

    part_one: int = solve(data)

    print(f'Part I: {part_one}')

