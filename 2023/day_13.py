sample = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def part1(inp):
    patterns = [pattern.splitlines() for pattern in inp.split("\n\n")]

    result = 0

    for pattern in patterns:
        for i in range(0, len(pattern[0]) - 1):
            ref = reflects(i, pattern)
            ref_v = reflects_vertically(i, pattern)
            if ref:
                print(ref)
                result += ref[0]
            if ref_v:
                print(ref_v)
                result += ref_v[0] * 100

    return result


def reflects(i, pattern):
    reflectors = []
    j = i + 1
    while True:
        if i < 0:
            return

        try:
            if [row[i] for row in pattern] != [row[j] for row in pattern]:
                return []
            reflectors.extend([i + 1, j + 1])
        except IndexError:
            return reflectors

        i -= 1
        j += 1


def reflects_vertically(i, pattern):
    reflectors = []
    j = i + 1
    while True:
        if i < 0:
            return

        try:
            if pattern[i] != pattern[j]:
                return []
            reflectors.extend([i + 1, j + 1])
        except IndexError:
            return reflectors

        i -= 1
        j += 1


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_13_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(sample)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
