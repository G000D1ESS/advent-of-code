from collections import deque


def load(filename) -> list[list[str]]:
    with open(filename) as file:
        mappa: list[list[str]] = []
        for line in file.readlines():
            line: list[str] = list(line.strip())
            mappa.append(line)
        return mappa


def solve(mappa: list[list[str]]) -> tuple[int, int]:
    splitted: int = 0
    timelines: int = 0

    n: int = len(mappa)
    m: int = len(mappa[0])
    scores: list[list[int]] = [[0]*m for _ in range(n)]

    start: tuple[int, int] = [(0, jdx) for jdx, val in enumerate(mappa[0]) if val == 'S'][0]
    queue: list[tuple[int, int]] = deque([start])

    while queue:
        row, col = queue.popleft()

        if not (0 <= row <= n-1 and 0 <= col <= m-1):
            timelines += 1
            continue

        if mappa[row][col] in '.S':
            mappa[row][col] = '|'
            queue.append((row+1, col))
            continue

        if mappa[row][col] == '^':
            splitted += 1
            mappa[row][col] = '#'
            queue.append((row, col-1))
            queue.append((row, col+1))
            continue

    return splitted, timelines


if __name__ == '__main__':
    filename: str = 'example.txt'
    # filename: str = 'puzzle.txt'

    mappa: list[list[str]] = load(filename)

    part_one, part_two = solve(mappa)
    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')

    print('\nMappa:')
    for row in mappa:
        print(''.join(row))


