import math
import multiprocessing
import random
import time

from shared import PuzzleInput, load

WORKERS: int = 14
FIND_TIME_WINDOW: float = 15.0

MAX_STEPS: int = int(1e9)

TEMP_START: float = 100.0
TEMP_END: float = 1e-9
COEF_STEP: int = 100
PLACES_TO_SWAP: int = 10
COOLING_FACTOR: float = 0.9999


def cast_buttons_to_list(buttons: list[int], lights_count: int) -> list[list[int]]:
    transformed: list[list[int]] = []

    for button in buttons:
        switches_str: str = bin(button)[2:].zfill(lights_count)
        switches_lst: list[int] = list(map(int, list(switches_str)))
        transformed.append(switches_lst)

    return transformed


def calc(state: list[int], buttons: list[list[int]], lights_count: int) -> list[int]:
    result: list[int] = [0] * lights_count

    for coef, button in zip(state, buttons):
        for idx, switched in enumerate(button):
            result[idx] += switched * coef

    return result


def get_energy(state: list[int], buttons: list[list[int]], wanted: list[int]) -> int:
    current: list[int] = calc(state, buttons, len(wanted))
    error: int = sum(abs(x - y) for x, y in zip(current, wanted))

    if error:
        return 10 ** 9 * error

    coef_sum: int = sum(state)
    return 10 ** 4 * coef_sum * coef_sum


def get_neighbor(state, T, max_joltage):
    new_state = state[:]
    num_changes = random.randint(1, PLACES_TO_SWAP)
    for _ in range(num_changes):
        i = random.randint(0, len(state)-1)
        step = max(1, int(T * COEF_STEP))
        new_state[i] += random.randint(-step, step)
        new_state[i] = max(0, new_state[i])
        new_state[i] = min(max_joltage, new_state[i])
    return new_state


def sa_worker(puzzle, timeout):
    start_time = time.time()

    best_state, best_energy = None, float('inf')
    max_joltage = max(puzzle.joltage)

    buttons = cast_buttons_to_list(puzzle.light_buttons, len(puzzle.joltage))

    while time.time() - start_time < timeout:
        state = [random.randint(0, max(puzzle.joltage)) for _ in range(len(puzzle.light_buttons))]
        energy = get_energy(state, buttons, puzzle.joltage)

        T = TEMP_START
        while T > TEMP_END and time.time() - start_time < timeout:
            new_state = get_neighbor(state, T, max_joltage)
            new_energy = get_energy(new_state, buttons, puzzle.joltage)
            dt_energy = new_energy - energy
            if dt_energy < 0 or random.random() < math.exp(-dt_energy / T):
                state = new_state
                energy = new_energy
                if energy < best_energy:
                    current: list[int] = calc(state, buttons, len(puzzle.joltage))
                    if current == puzzle.joltage:
                        best_state = state
                        best_energy = energy
            T *= COOLING_FACTOR

    return best_state, best_energy


def solve_parallel(puzzle):
    with multiprocessing.Pool(WORKERS) as pool:
        results = [pool.apply_async(sa_worker, (puzzle, FIND_TIME_WINDOW)) for _ in range(WORKERS)]
        output = [r.get() for r in results]

    best_state, best_energy = min(output, key=lambda x: x[1])
    if best_state is None:
        return -1

    print(f'[!] {puzzle.joltage} -> best minimal: {sum(best_state)} (energy: {best_energy})')
    return sum(best_state)


def solve(puzzle: PuzzleInput) -> int:
    # preparation
    wanted_result: list[int] = puzzle.joltage
    lights_count: int = len(wanted_result)
    max_joltage: int = max(puzzle.joltage)

    buttons: list[list[int]] = cast_buttons_to_list(puzzle.light_buttons, lights_count)
    buttons_count: int = len(buttons)

    # let's fire this puzzle!
    state: list[int] = [random.randint(0, max_joltage) for _ in range(buttons_count)]
    energy: float = get_energy(state, buttons, wanted_result)

    best_state = state
    best_energy = energy

    T = TEMP_START

    for step in range(MAX_STEPS):
        if T < TEMP_END:
            break

        # generate new state
        new_state = get_neighbor(state, T, max_joltage)
        new_energy = get_energy(new_state, buttons, wanted_result)

        dt_energy = new_energy - energy

        # change state
        if dt_energy < 0 or random.random() < math.exp(-dt_energy / T):
            state = new_state
            energy = new_energy

            # updating best result
            if energy < best_energy:
                best_state = state
                best_energy = energy

        # Охлаждаем
        T *= COOLING_FACTOR

    # print('*' * 60)
    # print('Current:\t', calc(best_state, buttons, lights_count))
    # print('Needed:\t\t', puzzle.joltage)
    # print('Used:\t\t', best_state, f'-> sum:', sum(best_state))
    # print('*' * 60)
    return best_state, calc(best_state, buttons, lights_count), wanted_result


def solve_puzzle(puzzle_data: list[PuzzleInput]) -> int:
    total: int = 0
    for puzzle in puzzle_data:
        idx: int = 0
        minimal: int = int(1e6)

        while idx < FIND_MIN_STEPS:
            best_state, current_result, wanted_result = solve(puzzle)

            if current_result != wanted_result:
                # print('-' * 80)
                # print('Rerun due to founded error')
                # print('-' * 80)
                continue

            minimal = min(minimal, sum(best_state))
            idx += 1

        print(f'[!] {wanted_result} -> best minimal: {minimal}')
        total += minimal
    return total


def solve_puzzlev2(puzzle_data: list[PuzzleInput]) -> int:
    total: int = 0
    for puzzle in puzzle_data:
        result = solve_parallel(puzzle)
        while result == -1:
            print(f'Rerun: {puzzle.joltage}')
            result = solve_parallel(puzzle)
        total += result
    return total


if __name__ == '__main__':
    # filename: str = 'example.txt'
    filename: str = 'puzzle.txt'

    puzzle_data: list[PuzzleInput] = load(filename)

    # part_two: int = solve_puzzle(puzzle_data)
    part_two: int = solve_puzzlev2(puzzle_data)
    print(f'Part II: {part_two}')

