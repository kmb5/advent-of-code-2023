from itertools import cycle

sample1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

sample2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

sample3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def parse(inp):
    parsed_map = {}

    dirs, map_ = inp.split("\n\n")

    for line in map_.splitlines():
        source, dests = line.split(" = ")
        parsed_map[source] = dests.replace("(", "").replace(")", "").split(", ")

    dirs = cycle(dirs)

    return dirs, parsed_map


def part1(inp):
    dirs, parsed_map = parse(inp)
    nextkey = "AAA"
    num_steps = 0

    while True:
        num_steps += 1
        direction = next(dirs)
        idx = 0 if direction == "L" else 1
        nextkey = parsed_map[nextkey][idx]
        if nextkey == "ZZZ":
            return num_steps


def part2(inp):
    dirs, parsed_map = parse(inp)
    num_steps = 0
    next_keys = [k for k in parsed_map if k.endswith("A")]

    while True:
        num_steps += 1
        direction = next(dirs)
        idx = 0 if direction == "L" else 1
        next_keys = set(parsed_map[k][idx] for k in next_keys)
        zend = set(k.endswith("Z") for k in next_keys)
        print(num_steps, " - ", len(zend), "/", len(next_keys))
        if all(zend):
            return num_steps


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_8_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
