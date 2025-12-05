

def load(filename) -> tuple[list[tuple[int, int]], list[int]]:
    with open(filename) as file:
        fresh_ingredients: list[tuple[int, int]] = []
        ingredients: list[int] = []

        for line in file.readlines():
            line: str = line.strip()
            if not line:
                continue

            if '-' in line:
                start_id, end_id = map(int, line.split('-'))
                fresh_ingredients.append((start_id, end_id))
                continue

            item_id: int = int(line)
            ingredients.append(item_id)

        fresh_ingredients.sort()
        merged: list[tuple[int, int]] = []

        for start, end in fresh_ingredients:
            if not merged:
                merged.append((start, end))
                continue

            pstart, pend = merged[-1]
            if pstart <= start <= pend:
                merged[-1] = (pstart, max(pend, end))
                continue

            merged.append((start, end))

        merged.sort()
        return merged, ingredients


def lookup(fresh_ingredients: list[tuple[int, int]], item_id: int) -> bool:
    n: int = len(fresh_ingredients)

    l: int = 0
    r: int = n-1

    while l <= r:
        m: int = (l+r) // 2

        s, e = fresh_ingredients[m]

        if s <= item_id <= e:
            return True

        if item_id < s:
            r = m - 1
        else:
            l = m + 1

    return False


def part_one(fresh_ingredients: list[tuple[int, int]], ingredients: list[int]) -> int:
    fresh: int = 0

    for item_id in ingredients:
        if lookup(fresh_ingredients, item_id):
            fresh += 1

    return fresh

def part_two(fresh_ingrediens: list[tuple[int, int]]) -> int:
    total: int = 0
    for start_id, end_id in fresh_ingredients:
        total += end_id - start_id + 1
    return total


if __name__ == '__main__':
    fresh_ingredients, ingredients = load('example.txt')

    part_one_: int = part_one(fresh_ingredients, ingredients)
    part_two_: int = part_two(fresh_ingredients)

    print(f'Part I: {part_one_}')
    print(f'Part II: {part_two_}')
