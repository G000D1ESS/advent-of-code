import itertools


def load(filename) -> list[tuple[int, int]]:
    with open(filename) as file:
        data: str = file.read()

        product_ids: list[tuple[int, int]] = []
        for ids_range in data.split(','):
            start_id, end_id = map(int, ids_range.split('-'))

            if len(str(start_id)) == len(str(end_id)):
                product_ids.append((start_id, end_id))
                continue

            mn_log10: int = len(str(start_id)) - 1
            mx_log10: int = len(str(end_id)) - 1

            ranges: list[int] = [start_id, end_id]
            for i in range(mn_log10, mx_log10+1):
                level: int = 10 ** i
                for subpair in [level, level-1]:
                    if start_id <= subpair <= end_id:
                        ranges.append(subpair)

            ranges.sort()
            for pair in itertools.batched(ranges, n=2):
                product_ids.append(pair)

        return product_ids


def first(product_ids: list[tuple[int, int]]) -> int:
    result: int = 0

    for block_start, block_end in product_ids:
        n: int = len(str(block_start))
        if n % 2 == 1:
            continue

        half: str = str(block_start)[:n//2]

        while int(half + half) <= block_end:
            if int(half + half) >= block_start:
                result += int(half + half)
            half = str(int(half) + 1)

    return result


def second(product_ids: list[tuple[int, int]]) -> int:
    result: int = 0

    for block_start, block_end in product_ids:
        for num in range(block_start, block_end+1):
            num_str: str = str(num)
            n: int = len(num_str)

            for groups in range(2, n+1):
                if n % groups != 0:
                    continue

                size: int = n // groups
                head: str = num_str[:size]

                if num_str.count(head) == groups:
                    result += num
                    break

    return result

def main() -> None:
    filename: str = 'example.txt'
    product_ids: list[tuple[int, int]] = load(filename)

    part_one: int = first(product_ids)
    part_two: int = second(product_ids)

    print(f'Part I: {part_one}')
    print(f'Part II: {part_two}')


if __name__ == '__main__':
    main()
