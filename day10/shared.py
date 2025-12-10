import re
from dataclasses import dataclass


@dataclass
class PuzzleInput:
    indicator: int
    light_buttons: list[int]
    joltage: list[int]


def load(filename: str) -> list[PuzzleInput]:
    with open(filename) as file:
        data: list[PuzzleInput] = []

        for line in file.readlines():
            match = re.search(r'(\[.+])(.+)({.+})', line.strip())

            indicator_raw: str = match[1].strip().strip('[]')
            buttons_raw: list[str] = match[2].strip().split()
            joltage_raw: str = match[3].strip().strip('{}')

            n: int = len(indicator_raw)
            indicator: int = 0
            for power, ch in enumerate(indicator_raw[::-1]):
                if ch == '#':
                    indicator += 2 ** power

            light_buttons: list[int] = []
            for buttons in buttons_raw:
                lights_raw: list[str] = buttons.strip().strip('()').split(',')

                lights: int = 0
                for power in map(int, lights_raw):
                    lights += 2 ** (n - power - 1)

                light_buttons.append(lights)

            joltage: list[int] = list(map(int, joltage_raw.split(',')))

            puzzle_input = PuzzleInput(
                indicator=indicator,
                light_buttons=light_buttons,
                joltage=joltage,
            )
            data.append(puzzle_input)

        return data