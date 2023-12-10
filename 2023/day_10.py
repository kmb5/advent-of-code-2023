sample = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".splitlines()

sample2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()


def find_start(inp):
    for i, row in enumerate(inp):
        for j, cell in enumerate(row):
            if cell == "S":
                return i, j


def next_idx(prev_idx, curr_idx, c):
    if c == "|":
        if prev_idx[0] < curr_idx[0]:
            return curr_idx[0] + 1, curr_idx[1]  # 1, 0
        return curr_idx[0] - 1, curr_idx[1]  # -1, 0
    if c == "-":
        if prev_idx[1] < curr_idx[1]:
            return curr_idx[0], curr_idx[1] + 1  #  0, 1
        return curr_idx[0], curr_idx[1] - 1  # 0, -1
    if c == "L":
        if prev_idx[0] < curr_idx[0]:
            return curr_idx[0], curr_idx[1] + 1  # 0, 1
        return curr_idx[0] - 1, curr_idx[1]  # -1, 0
    if c == "J":
        if prev_idx[0] < curr_idx[0]:
            return curr_idx[0], curr_idx[1] - 1  # 0, -1
        return curr_idx[0] - 1, curr_idx[1]  # -1, 0
    if c == "7":
        if prev_idx[1] < curr_idx[1]:
            return curr_idx[0] + 1, curr_idx[1]  # 1, 0
        return curr_idx[0], curr_idx[1] - 1  # 0, -1
    if c == "F":
        if prev_idx[0] > curr_idx[0]:
            return curr_idx[0], curr_idx[1] + 1
        return curr_idx[0] + 1, curr_idx[1]


def find_connecting_to_start(inp, start):
    """|    -   L    J   7    F"""
    connecting = []
    si, sj = start
    if inp[si + 1][sj] in ("L", "J", "|"):
        # above
        connecting.append((si + 1, sj))
    if inp[si - 1][sj] in ("|", "7", "F"):
        # below
        connecting.append((si - 1, sj))
    if inp[si][sj - 1] in ("-", "F", "L"):
        connecting.append((si, sj - 1))
    if inp[si][sj + 1] in ("-", "J", "7"):
        connecting.append((si, sj + 1))
    return connecting


def part1(inp):
    prev = find_start(inp)
    curr = find_connecting_to_start(inp, prev)[0]
    path = traverse_pipes(prev, curr, inp)
    mid = (len(path) - 1) // 2
    return path[mid]


def traverse_pipes(prev, start, inp):
    curr = start
    trav_len = 0
    travs = []
    while True:
        currChar = inp[curr[0]][curr[1]]
        print(currChar, curr)
        if currChar == "S":
            break
        _curr = curr
        curr = next_idx(prev, curr, currChar)
        prev = _curr
        trav_len += 1
        travs.append(trav_len)
    return travs


def part2(inp):
    pass


def test_navi():
    assert next_idx((0, 0), (0, 1), "7") == (1, 1)
    assert next_idx((1, 1), (0, 1), "7") == (0, 0)

    assert next_idx((1, 0), (0, 0), "F") == (0, 1)
    assert next_idx((0, 1), (0, 0), "F") == (1, 0)

    assert next_idx((0, 0), (1, 0), "L") == (1, 1)
    assert next_idx((1, 1), (1, 0), "L") == (0, 0)

    assert next_idx((0, 1), (1, 1), "J") == (1, 0)
    assert next_idx((1, 0), (1, 1), "J") == (0, 1)

    assert next_idx((0, 0), (0, 1), "-") == (0, 2)
    assert next_idx((0, 2), (0, 1), "-") == (0, 0)

    assert next_idx((0, 0), (1, 0), "|") == (2, 0)
    assert next_idx((2, 0), (1, 0), "|") == (0, 0)


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_10_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read().splitlines()

    test_navi()
    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
