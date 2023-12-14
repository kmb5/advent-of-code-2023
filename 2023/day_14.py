sample = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def parse(inp):
    return [list(row) for row in inp.splitlines()]


moves = {"n": ()}


def move_rock(lst, x, y, d="n", i=1):
    if d == "n":
        newx, newy = x - i, y
    elif d == "s":
        newx, newy = x + i, y
    elif d == "e":
        newx, newy = x, y - i
    elif d == "w":
        newx, newy = x, y + i
    else:
        raise ValueError("unknown direction")

    if newx < 0 or newx >= len(lst) or newy < 0 or newy >= len(lst[0]):
        return i - 1

    nxt = lst[newx][y]
    if nxt != ".":
        return i - 1
    return move_rock(lst, x, y, d, i + 1)


# pylint: disable=consider-using-enumerate
def tilt(lst, d="n"):
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if lst[i][j] != "O":
                continue

            offset = move_rock(lst, i, j, d)
            if offset > 0:
                if d == "n":
                    lst[i - offset][j] = "O"
                elif d == "s":
                    lst[i + offset][j] = "O"
                elif d == "e":
                    lst[i][j - offset] = "O"
                elif d == "w":
                    lst[i][j + offset] = "O"

                lst[i][j] = "."

    return lst


def calc_load(lst):
    sum_load = 0
    ln = len(lst)
    for i, row in enumerate(lst):
        l = (ln - i) * len([i for i in row if i == "O"])
        sum_load += l

    return sum_load


def part1(inp):
    parsed = parse(inp)
    tilted = tilt(parsed)
    return calc_load(tilted)


def part2(inp):
    from tqdm import tqdm

    parsed = parse(inp)
    tilted = parsed
    tilts = "nwse"
    for _ in tqdm(range(1000000000)):
        for d in tilts:
            tilted = tilt(tilted, d)

    return calc_load(tilted)


def test_move():
    inp = parse(sample)
    assert move_rock(inp, 0, 0) == 0
    assert move_rock(inp, 1, 0) == 0
    assert move_rock(inp, 1, 2) == 1
    assert move_rock(inp, 1, 3) == 1
    assert move_rock(inp, 3, 0) == 1
    assert move_rock(inp, 3, 1) == 3
    assert move_rock(inp, 3, 9) == 1
    assert move_rock(inp, 9, 1) == 4
    assert move_rock(inp, 9, 2) == 2


def main():
    test_move()

    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_14_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    print(move_rock(parse(inp), 6, 2))

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
