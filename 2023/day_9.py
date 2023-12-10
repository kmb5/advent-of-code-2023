sample = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def parse(inp):
    return [list(map(int, line.split())) for line in inp.splitlines()]


def run_prediction(line, preds=None):
    if preds is None:
        preds = []

    diffs = [line[i] - line[i - 1] for i in range(1, len(line))]
    preds.append(diffs)
    if any(diffs):
        run_prediction(diffs, preds)

    return preds


def extrapolate(preds):
    result = 0
    for pred in reversed(preds):
        result += pred[-1]
    return result


def extrapolate_backwards(preds):
    result = 0
    for i in range(len(preds) - 1, 0, -1):
        result = preds[i - 1][0] - result
    return result


def part1(inp):
    sum_nexts = 0
    parsed = parse(inp)
    for line in parsed:
        preds = run_prediction(line)
        next_value = extrapolate(preds) + line[-1]
        sum_nexts += next_value
    return sum_nexts


def part2(inp):
    sum_prevs = 0
    parsed = parse(inp)
    for line in parsed:
        preds = run_prediction(line)
        prev_value = extrapolate_backwards(preds)
        sum_prevs += line[0] - prev_value

    return sum_prevs


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_9_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(inp)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
