
M: int = 100
START_POINT: int = 50


def load(filename) -> list[tuple[bool, int]]:
    with open(filename) as file:
        data = file.read()

        commands = []
        for line in data.splitlines():
            clockwise: bool = line[0] == 'R'
            degree: int = int(line[1:])
            commands.append((clockwise, degree))

        return commands


def solve(commands: list[tuple[bool, int]], multiclick: bool) -> int:
    password: int = 0
    current: int = START_POINT

    for clockwise, degree in commands:
        cycles, degree = divmod(degree, M)
        password += cycles

        if not clockwise:
            degree *= -1

        if (
                multiclick
                and current != 0
                and (current + degree >= M or current + degree <= 0)
        ):
            password += 1


        current = (current + degree + M) % M

        if not multiclick:
            password -= cycles
            password += int(current == 0)

    return password


if __name__ == '__main__':
    commands: list[tuple[bool, int]] = load('example.txt')

    part_one: int = solve(commands, multiclick=False)
    part_two: int = solve(commands, multiclick=True)

    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')

