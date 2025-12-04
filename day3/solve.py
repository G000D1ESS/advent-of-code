def load(filename):
    with open(filename) as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def solve(batteries: list[str], window: int) -> int:
    joltage: int = 0

    for battery in batteries:
        m: int = window
        n: int = len(battery)

        # dp[m][n]: m - used, n - offset
        dp: list[list[int]] = [[0] * (n+1) for i in range(m+1)]

        for i in range(1, n+1):
            curr: int = int(battery[i-1])

            for k in range(1, m+1):
                new: int = (10 * dp[k-1][i-1]) + curr
                dp[k][i] = max(new, dp[k][i-1])

        joltage += dp[m][n]

    return joltage


if __name__ == '__main__':
    batteries: list[str] = load('example.txt')

    part_one: int = solve(batteries, window=2)
    part_two: int = solve(batteries, window=12)

    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')
