def part1(inp):
    result = 0
    for line in inp.splitlines():
        digits = [c for c in line if c.isdigit()]
        result += int(f"{digits[0]}{digits[-1]}")

    return result


def extend_words_with_digits(text: str):
    REPLACEMENTS = {
        "one": "on1e",
        "two": "tw2o",
        "three": "thr3ee",
        "four": "fo4ur",
        "five": "fi5ve",
        "six": "si6x",
        "seven": "sev7en",
        "eight": "ei8ght",
        "nine": "ni9ne",
    }

    txt = text

    for old, new in REPLACEMENTS.items():
        txt = txt.replace(old, new)

    return txt


def part2(inp):
    result = 0
    for line in inp.splitlines():
        replaced_line = extend_words_with_digits(line)
        digits = [c for c in replaced_line if c.isdigit()]
        result += int(f"{digits[0]}{digits[-1]}")

    return result


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_1_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
