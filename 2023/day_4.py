from copy import deepcopy
from pprint import pprint

sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def parse(txt: str) -> list[set[int]]:
    parsed = []
    for row in txt.splitlines():
        _, nums = row.split(":")
        winning, mine = nums.split(" | ")
        parsed.append(
            [
                set(int(n) for n in winning.split()),
                set(int(n) for n in mine.split()),
            ]
        )
    return parsed


def part1(inp):
    sum_pts = 0
    parsed = parse(inp)
    for game in parsed:
        winning, mine = game
        num_won = len(winning.intersection(mine))
        if num_won > 0:
            sum_pts += 2 ** (num_won - 1)
    return sum_pts


def part2(inp):
    parsed = parse(inp)
    games: dict[int, list] = {i + 1: game for i, game in enumerate(parsed)}

    num_each = {i: 1 for i in games.keys()}  # how many sets do we have from each card

    for i, game in games.items():
        winning, mine = game
        num_won = len(winning.intersection(mine))
        for _ in range(num_each[i]):  # process original card and all copies
            for j in range(i + 1, i + num_won + 1):
                # add a copy for each won card below
                num_each[j] += 1

    return sum(num_each.values())


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_4_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
