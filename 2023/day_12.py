from itertools import product
from tqdm import tqdm

sample = ".###..##.#.# 3,2,1"
sample2 = "?###???????? 3,2,1"
sample3 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def get_all_combinations(s: str) -> list[str]:
    for p in map(iter, product(".#", repeat=s.count("?"))):
        comb = "".join(c if c != "?" else next(p) for c in s)
        if is_valid_combination(comb):
            yield comb


def is_valid_combination(s: str) -> bool:
    springs, groups = s.split()

    damaged_groups = [x for x in springs.split(".") if x != ""]
    group_nums = groups.split(",")

    if len(damaged_groups) != len(group_nums):
        return False

    for i, group in enumerate(damaged_groups):
        try:
            if len(group) != int(group_nums[i]):
                return False
        except IndexError:
            return False
    return True


def unfold(row: str) -> list[str]:
    springs, nums = row.split()

    return "?".join([springs] * 5) + " " + ",".join([nums] * 5)


def part1(inp):
    total_num_arrangements = 0
    for row in tqdm(inp.splitlines()):
        num_arrangements = len(list(get_all_combinations(row)))
        total_num_arrangements += num_arrangements
    return total_num_arrangements


def part2(inp):
    total_num_arrangements = 0
    for row in tqdm(inp.splitlines()):
        unfolded = unfold(row)
        num_arrangements = len(list(get_all_combinations(unfolded)))
        total_num_arrangements += num_arrangements

    return total_num_arrangements


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_12_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    # part1_sol = part1(inp)
    # print("Part 1: ", part1_sol)

    part2_sol = part2(sample3)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
