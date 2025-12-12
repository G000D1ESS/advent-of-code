from functools import lru_cache


def load(filename: str) -> dict[set[str]]:
    with open(filename) as file:
        mapp: dict[set[str]] = {}

        for line in file.readlines():
            source, _, destinations = line.strip().partition(':')
            mapp[source] = set(destinations.strip().split(' '))

        return mapp


def part_one(mapp: dict[set[str]]):

    start: str = 'you'
    end: str = 'out'


    visited: set[str] = set()

    def dfs(vertex, final):
        if vertex == final:
            return 1

        pathes: int = 0
        children: set[str] = mapp[vertex]

        for child in children:
            if child in visited:
                continue

            visited.add(child)
            pathes += dfs(child, final)
            visited.remove(child)

        return pathes


    total: int = dfs(start, end)
    return total


def part_two(mapp: dict[set[str]]):

    start: str = 'svr'
    end: str = 'out'


    visited: set[str] = set()
    required: frozenset[str] = frozenset({'dac', 'fft'})

    @lru_cache(maxsize=1024)
    def dfs(vertex: str, final: str, checkpoints: frozenset[int]):
        if vertex in required:
            checkpoints = frozenset(checkpoints | {vertex})

        if vertex == final:
            if required == checkpoints:
                return 1
            return 0

        total: int = 0
        children: set[str] = mapp[vertex]
        for child in children:
            if child in visited:
                continue

            visited.add(child)
            total += dfs(child, final, checkpoints)
            visited.remove(child)
        return total


    total: int = dfs(start, end, frozenset())
    print('(?) LRU Cache:', dfs.cache_info())
    return total


if __name__ == '__main__':
    filename: str = 'puzzle.txt'

    mapp: dict[set[str]] = load(filename)

    part_one_: int = part_one(mapp)
    print(f'Part I: {part_one_}')

    part_two_: int = part_two(mapp)
    print(f'Part II: {part_two_}')

