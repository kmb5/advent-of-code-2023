import networkx as nx
from itertools import combinations, accumulate

sample = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def expand(inp: str):
    inp: list = inp.splitlines()
    empty_row_idxs = [i for i in range(len(inp)) if inp[i] == len(inp[i]) * "."]
    cols = ["".join(row[i] for row in inp) for i in range(len(inp[0]))]
    empty_col_idxs = [i for i in range(len(cols)) if cols[i] == len(cols[i]) * "."]
    for ridx in empty_row_idxs:
        inp.insert(ridx + 1, "." * len(inp[ridx]))

    rnd = 0
    for cidx in empty_col_idxs:
        for i, row in enumerate(inp):
            _cidx = cidx + rnd
            inp[i] = row[:_cidx] + "." + row[_cidx:]

        rnd += 1

    return inp


def parse(inp):
    nodes = []
    for i, row in enumerate(inp):
        for j, col in enumerate(row):
            if col == "#":
                nodes.append((i, j))
    return nodes


def part1(inp):
    inp = expand(inp)
    nodes = parse(inp)

    sum_lengths = 0
    all_pairs = combinations(nodes, 2)
    for pair in all_pairs:
        a, b = pair
        ax, ay = a
        bx, by = b
        sum_lengths += abs(bx - ax) + abs(by - ay)

    return sum_lengths


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_11_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(sample)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
