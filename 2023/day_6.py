sample = """Time:      7  15   30
Distance:  9  40  200"""


def parse(inp: str):
    times, distances = inp.splitlines()

    _, times = times.split(":")
    _, distances = distances.split(":")

    return {int(t): int(distances.split()[i]) for i, t in enumerate(times.split())}


def parse_p2(inp: str):
    time, distance = inp.splitlines()
    _, time = time.split(":")
    _, distance = distance.split(":")
    return {int(time.replace(" ", "")): int(distance.replace(" ", ""))}


def part1(inp):
    multiples = 1

    for time, distance in inp.items():
        min_hold = None
        for hold in range(time + 1):
            traveled = hold * (time - hold)
            if traveled > distance:
                min_hold = hold
                break

        max_hold = time - hold
        num_ways = max_hold - min_hold + 1
        multiples *= num_ways

    return multiples


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_6_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(parse(inp))
    print("Part 1: ", part1_sol)

    part2_sol = part1(parse_p2(inp))
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
