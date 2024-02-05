sample = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

filltest = [
    "...#######...........#####.....................########...................########....#......#####................"
]

MAPSIZE = (20, 20)  # (3500, 5000)
START_COORDS = (5, 5)  #  (1000, 500)


def parse(inp):
    result = []
    for line in inp.splitlines():
        d, n, c = line.split()
        n = int(n)
        c = c.replace("(", "").replace(")", "")
        result.append((d, n, c))

    return result


def reduce_size(printable):
    """only for convenience"""
    new_map = []
    starts = []
    ends = []
    for row in printable:
        try:
            starts.append(row.index("#"))
            ends.append(row.rindex("#"))
        except ValueError:
            continue

    start = min(starts)
    end = max(ends)

    for row in printable:
        if row == "." * len(row):
            continue
        new_map.append(row[start : end + 1])

    return new_map


def left(n, x, y, color, dig_map):
    for it in range(n):
        dig_map[y][x - it] = color
    return x - n, y


def right(n, x, y, color, dig_map):
    for it in range(n):
        dig_map[y][x + it] = color
    return x + n, y


def up(n, x, y, color, dig_map):
    for it in range(n):
        dig_map[y - it][x] = color
    return x, y - n


def down(n, x, y, color, dig_map):
    for it in range(n):
        dig_map[y + it][x] = color
    return x, y + n


def calc_cubic_meters(dig_map: list[str]):
    cnt = 0
    for row in dig_map:
        for col in row:
            if col == "#":
                cnt += 1
    return cnt


INSTRUCTION_MAP = {"L": left, "D": down, "R": right, "U": up}


def repl(m):
    return "#" * len(m.group())


def fill(inp):
    import re

    filled = []
    for row in inp:
        filled.append(re.sub(r"#\.+#", repl, row))
    return filled


def part1(inp):
    m_x, m_y = MAPSIZE
    s_x, s_y = START_COORDS
    dig_map = [["." for _ in range(m_x)] for _ in range(m_y)]
    dig_map[s_x][s_y] = None  # starts with 1 cube at 0,0, no color

    parsed = parse(inp)
    for row in parsed:
        direction, num, color = row
        s_x, s_y = INSTRUCTION_MAP[direction](num, s_x, s_y, color, dig_map)

    dig_map = simplify(dig_map)
    reduced = reduce_size(dig_map)
    print_dig_map(reduced)
    mapb = mapback(reduced)
    print_dig_map(mapb)
    filled = fillup(mapb)
    print_dig_map(filled)
    return calc_cubic_meters(filled)


def mapback(arr):
    res = []
    for row in arr:
        res.append([char for char in row])
    return res


def simplify(dig_map):
    res = []
    for row in dig_map:
        to_add = ""
        for cell in row:
            if cell == ".":
                to_add += "."
            else:
                to_add += "#"
        res.append(to_add)

    return res


def print_dig_map(simplified):
    for row in simplified:
        print(row)


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_18_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(sample)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
