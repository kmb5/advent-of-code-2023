sample = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def parse(inp: str):
    parsed = []
    start = (0, 0)
    for i, row in enumerate(inp.splitlines()):
        if "S" in row:
            start = i, row.index("S")
        parsed.append(row)
    return parsed, start


def possible_steps(positions: set[tuple[int]], garden: set[str]):
    steps = set()
    for position in positions:
        x, y = position
        if y > 0 and garden[y - 1][x] == ".":
            steps.add((x, y - 1))
        if y < len(garden) and garden[y + 1][x] == ".":
            steps.add((x, y + 1))
        if x > 0 and garden[y][x - 1] == ".":
            steps.add((x - 1, y))
        if x < len(garden[0]) and garden[y][x + 1] == ".":
            steps.add((x + 1, y))

    return steps


def print_map(positions, garden):
    for y, row in enumerate(garden):
        printable = ""
        for x, cell in enumerate(row):
            if (x, y) in positions:
                printable += "O"
            else:
                printable += cell

        print(printable)


def part1(inp):
    parsed, start = parse(inp)
    psteps = set([start])
    for _ in range(64):
        psteps = possible_steps(psteps, parsed)
        print_map(psteps, parsed)
        print(len(psteps) + 1)


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_21_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
