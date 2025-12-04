from copy import deepcopy


def load(filename) -> list[list[str]]:
    with open(filename) as file:
        lines: list[str] = []

        for line in file.readlines():
            line = '#' + line.strip() + '#'
            lines.append(list(line))

        border = ['#'] * len(max(lines))
        lines = [border] + lines + [border]
        return lines


def solve(paper_rolls: list[list[str]], cycles: int) -> int:
    n: int = len(paper_rolls)
    m: int = len(paper_rolls[0])
    paper_rolls: list[list[str]] = deepcopy(paper_rolls)

    moves: list[tuple[int, int]] = [
        (+0, -1), # L
        (+0, +1), # R
        (-1, +0), # U
        (+1, +0), # D
        (-1, -1), # LU
        (+1, -1), # LD
        (-1, +1), # RU
        (+1, +1), # RD
    ]

    accessable: int = 0

    for _ in range(cycles):
        to_remove: set[tuple[int, int]] = set()

        for i in range(n):
            for j in range(m):
                if paper_rolls[i][j] == '@':
                    cnt: int = 0
                    for x, y in moves:
                        if paper_rolls[i+x][j+y] == '@':
                            cnt += 1

                    if cnt < 4:
                        to_remove.add((i, j))

        if not to_remove:
            break

        for i, j in to_remove:
            accessable += 1
            paper_rolls[i][j] = '.'

    return accessable


if __name__ == '__main__':
    paper_rolls: list[str] = load('example.txt')

    part_one: int = solve(paper_rolls, cycles=1)
    part_two: int = solve(paper_rolls, cycles=1000)

    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')
