

def load_one(filename) -> tuple[list[list[int]], list[str]]:
    with open(filename) as file:
        *numbers, operations = file.readlines()

        operations: list[str] = operations.strip().split()

        n: int = len(operations)
        groups: list[list[int]] = [[] for _ in range(n)]

        for row in numbers:
            for idx, num in enumerate(map(int, row.split())):
                groups[idx].append(num)

        return groups, operations


def load_two(filename) -> tuple[list[list[int]], list[str]]:
    with open(filename) as file:
        data = file.readlines()

        operations: list[str] = []
        groups: list[list[int]] = []

        n: int = len(data)
        m: int = len(data[0])

        group: list[int] = []

        for col in range(m):
            if (col+1 == m) or (data[n-1][col] != ' '):
                if group:
                    groups.append(group)

                group = []
                operations.append(data[n-1][col])

            curr: list[str] = []
            for row in range(n-1):
                curr.append(data[row][col])

            num_str: str = ''.join(curr).strip()
            if num_str:
                group.append(int(num_str))

        return groups, operations


def solve(groups: list[list[int]], operations: list[str]) -> int:
    total: int = 0

    for group, oper in zip(groups, operations):
        n: int = len(group)
        curr: int = group[0]

        for i in range(1, n):
            if oper == '+':
                curr += group[i]
            elif oper == '*':
                curr *= group[i]

        total += curr

    return total


if __name__ == '__main__':
    filename: str = 'example.txt'

    groups, operations = load_one(filename)
    part_one: int = solve(groups, operations)
    print(f'Part I: {part_one}')

    groups, operations = load_two(filename)
    part_two: int = solve(groups, operations)
    print(f'Part II: {part_two}')

