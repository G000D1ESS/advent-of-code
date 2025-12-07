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


    def dfs(row: int, col: int) -> int:
        # exit case
        if not (0 <= row <= n-1 and 0 <= col <= m-1):
            return 1

        if mappa[row][col] == '|':
            return scores[row][col]

        if mappa[row][col] in '.S':
            score: int = dfs(row+1, col)
            scores[row][col] = score
            mappa[row][col] = '|'
            return score

        # splitter case: '^'
        mappa[row][col] = '#'
        score: int = dfs(row, col-1) + dfs(row, col+1)
        return score


    start_row: int = 0
    start_col: int = mappa[start_row].index('S')

    timelines: int = dfs(start_row, start_col)

    splitted: int = 0
    for row in mappa:
        splitted += row.count('#')

    return splitted, timelines


if __name__ == '__main__':
    filename: str = 'example.txt'

    mappa: list[list[str]] = load(filename)

    part_one, part_two = solve(mappa)
    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')

