sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def parse_input(inp: str):
    """return a tuple of seeds, all_maps"""
    lns = inp.split("\n\n")

    _, seeds = lns[0].split(": ")

    return seeds, lns[1:]


def calc_ranges(inp: str):
    """return all ranges in an input as a sorted dict with the offsets as values
    {
        0: 0
        50: +2,
        98: -48
        100: 0
    }
    """
    range_map = {0: 0}
    for rng in inp.splitlines():
        destination, source, rlen = (int(x) for x in rng.split())
        range_map[source] = -(source - destination)
        if source + rlen not in range_map:
            range_map[source + rlen] = 0

    return dict(sorted(range_map.items()))


def get_value(k, range_map):
    """use map from calc_ranges and get the key with the offset from the map, if exists
    if not, simply return k
    {
        0: 0
        50: +2,
        98: -48
        100: 0
    }"""

    rngs = list(range_map.keys())

    for i, rng in enumerate(rngs):
        try:
            if k < rngs[i + 1]:
                return k + range_map[rng]
        except IndexError:
            pass

    return k


def get_all_range_maps(inp: str):
    rngmaps = list()
    for mp in inp:
        _, rngmap = mp.split(":\n")
        ranges = calc_ranges(rngmap)
        rngmaps.append(ranges)
    return tuple(rngmaps)


def traverse_maps(num, rngmaps):
    curr_num = num
    for m in rngmaps:
        curr_num = get_value(curr_num, m)

    return curr_num


def part1(inp):
    seeds, maps = parse_input(inp)

    range_maps = get_all_range_maps(maps)

    loc_nums = []

    for seed in seeds.split():
        loc_num = traverse_maps(int(seed), range_maps)
        loc_nums.append(loc_num)

    return min(loc_nums)


def get_all_seeds_from_pairs(seeds):
    all_seeds = []
    seeds = seeds.split()

    for i in range(0, len(seeds), 2):
        seed = int(seeds[i])
        all_seeds.append([seed, int(seeds[i + 1])])

    return all_seeds


def part2(inp):
    """ugly brute force solution, don't even look at this.
    It needs ~3h to run fully, but you might get lucky if the minimum
    is among the first few seeds (as I print the current min every time)"""
    from tqdm import tqdm

    seeds, maps = parse_input(inp)

    seeds = get_all_seeds_from_pairs(seeds)

    range_maps = get_all_range_maps(maps)

    min_loc = None
    i = 3
    for start, end in seeds[i - 1 :]:
        print("Seed ", i, " current min: ", min_loc)
        for n in tqdm(range(start, start + end)):
            loc = traverse_maps(n, range_maps)
            if min_loc is None:
                min_loc = loc
            else:
                min_loc = min(loc, min_loc)

        i += 1

    return min_loc


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_5_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
