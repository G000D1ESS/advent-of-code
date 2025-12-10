from shared import load, PuzzleInput


def part_one(puzzle: PuzzleInput) -> int:
    buttons: list[int] = puzzle.light_buttons
    n: int = len(buttons)

    # dp[k][state] -> min cost of state with k-first buttons
    dp: list[dict[int, int]] = [dict() for _ in range(n+1)]

    # start -> all indicators off
    # penalty -> just 1 click
    dp[0][0] = 0
    penalty: int = 1

    for k in range(1, n+1):
        button_switches: int = buttons[k-1]
        prev_state: dict[int, int] = dp[k-1]
        curr_state: dict[int, int] = dp[k]

        # transfer previous state
        curr_state.update(prev_state)

        # get new states
        for state, cost in prev_state.items():
            use_cost: int = cost + penalty
            nxt_state: int = state ^ button_switches

            curr_state.setdefault(nxt_state, use_cost)
            curr_state[nxt_state] = min(curr_state[nxt_state], use_cost)

    required_state: int = puzzle.indicator
    return dp[n][required_state]


if __name__ == '__main__':
    filename: str = 'example.txt'

    puzzle_data: list[PuzzleInput] = load(filename)

    part_one_: int = sum(map(part_one, puzzle_data))
    print(f'Part I: {part_one_}')

